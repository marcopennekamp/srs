srsModule.controller('ReviewController', function ($http) {
    var controller = this;
    controller.inputString = '';

    // Go to the next word when the enter key is pressed.
    // This allows us to stop to give the user feedback on whether they
    // got their word right or wrong.
    controller.doNextOnEnter = false;

    // '': No feedback for this word yet.
    // 'correct': The meaning/reading was correct.
    // 'wrong': The meaning/reading was wrong.
    controller.feedback = '';

    controller.prompt = null;
    controller.word = null;
    controller.untouched = [];
    controller.started = [];
    controller.finished = [];

    controller.init = function () {
        wanakana.bind(document.getElementById('reading-input')); // Bind alphabet to kana conversion library to reading text field.
        $http.get('/api/review/words/all').then(function (res) {
            // TODO: Handle errors!
            controller.untouched = res.data;

            // Determine for all words whether they contain Kanji.
            // Should a word not include any Kanji, there is no reason
            // to prompt for the reading.
            // Also prepares each word for the review.
            for (var i = 0; i < controller.untouched.length; i += 1) {
                var word = controller.untouched[i];
                word.hasKanji = !!(word.readings.length > 1 || word.readings[0] != word.word);
                word.meaningStats = { isCorrect: false, tries: 0 };
                if (word.hasKanji) {
                    word.readingStats = { isCorrect: false, tries: 0 };
                }
            }

            // Fetch the first word.
            controller.next();
        });
    };

    controller.next = function () {
        controller.doNextOnEnter = false;
        controller.inputString = '';
        controller.feedback = '';

        var nextWord;
        if (controller.started.length >= 7) { // Cap maximum number of different words at any time during the review.
            nextWord = popRandomElement(controller.started);
        } else if (controller.untouched.length > 0) { // Otherwise select some word from the yet untouched words.
            nextWord = popRandomElement(controller.untouched);
        } else if (controller.started.length > 0) { // Finally, drain the pool of started items.
            nextWord = popRandomElement(controller.started);
        } else { // In this case we are finished with the reviews!
            // TODO: Check whether the server has new reviews.
            nextWord = null;
        }

        controller.word = nextWord;
        if (nextWord != null) {
            // We assume here that the word hasn't been fully cleared yet.
            if (nextWord.hasKanji) {
                if (nextWord.readingStats.isCorrect) {
                    controller.prompt = 'meaning';
                } else if (nextWord.meaningStats.isCorrect) {
                    controller.prompt = 'reading';
                } else {
                    // Both meaning and reading could be asked.
                    // Either balance reading and meaning in a margin of 2 tries.
                    // Or choose the prompt type at random.
                    var readingMeaningDiff = nextWord.readingStats.tries - nextWord.meaningStats.tries;
                    if (readingMeaningDiff > 1) { // Readings have been tried at least 2 times more often.
                        controller.prompt = 'meaning';
                    } else if (readingMeaningDiff < -1) { // Meanings have been tried at least 2 times more often.
                        controller.prompt = 'reading';
                    } else { // Fairly balanced, just ask for either.
                        if (Math.random() >= 0.5) {
                            controller.prompt = 'meaning';
                        } else {
                            controller.prompt = 'reading';
                        }
                    }
                }
            } else {
                controller.prompt = 'meaning';
            }
        } else {
            controller.prompt = null;
            controller.saveFinished();
        }
    };

    controller.checkMeaning = function () {
        controller.checkInput(controller.word, controller.word.meaningStats, controller.word.meanings)
    };

    controller.checkReading = function () {
        controller.checkInput(controller.word, controller.word.readingStats, controller.word.readings)
    };

    controller.checkInput = function(word, stats, allowedStrings) {
        if (controller.doNextOnEnter) {
            controller.next();
        } else {
            var input = controller.inputString;
            var valid = false;
            for (var i = 0; i < allowedStrings.length; i += 1) {
                if (input === allowedStrings[i]) {
                    valid = true;
                    break;
                }
            }

            if (valid) {
                stats.isCorrect = true;
                stats.tries += 1;
                controller.maybeFinishWord(word);
                controller.feedback = 'correct';
            } else {
                stats.tries += 1;
                controller.started.push(word);
                controller.feedback = 'wrong';
            }

            controller.doNextOnEnter = true;
        }
    };

    controller.maybeFinishWord = function(word) {
        if (word.meaningStats.isCorrect && (!word.hasKanji || word.readingStats.isCorrect)) { // Word is finished!
            var finishedWordData = {id: word.id, meaning_tries: word.meaningStats.tries};
            if (word.hasKanji) {
                finishedWordData.reading_tries = word.readingStats.tries;
            }
            controller.finished.push(finishedWordData);
        } else {
            controller.started.push(word);
        }
    };

    controller.finish = function () {
        controller.saveFinished();
    };

    controller.saveFinished = function () {
        var data = controller.finished;
        controller.finished = [];
        $http.put(
            '/api/review/finish',
            data
        ).then(
            function (res) { // Success
                alert('Your progress has been saved.');
            }, function (res) { // Error
                alert('An error occurred while trying to save the words as discovered.');
            }
        );
    };
});