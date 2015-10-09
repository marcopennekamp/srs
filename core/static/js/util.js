function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function popRandomElement(array) {
    return array.splice(getRandomInt(0, array.length), 1)[0];
}