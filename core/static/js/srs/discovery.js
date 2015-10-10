srsModule.controller('DiscoveryController', function ($http) {
    var controller = this;
    controller.currentWord = null;
    controller.queue = [];
    controller.finished = [];

    controller.init = function () {
        $http.get('/api/discover/words/all').then(function (res) {
            // TODO: Handle errors!
            controller.queue = res.data;
            controller.currentWord = controller.queue.pop();
        });
    };

    controller.next = function () {
        if (controller.queue.length > 0) {
            controller.finished.push(controller.currentWord.id);
            controller.currentWord = controller.queue.shift();
        } else {
            // TODO: Check if the server has any more words that could be discovered.
            controller.finished.push(controller.currentWord.id);
            controller.currentWord = null;
        }
    };

    controller.finish = function () {
        controller.saveFinished();
    };

    controller.saveFinished = function () {
        if (controller.finished.length > 0) {
            var words = controller.finished;
            controller.finished = [];
            $http.put(
                '/api/discover/finish',
                words
            ).then(
                function (res) { // Success
                    alert('Your progress has been saved.');
                }, function (res) { // Error
                    alert('An error occurred while trying to save the words as discovered.');
                }
            );
        }
    };
});