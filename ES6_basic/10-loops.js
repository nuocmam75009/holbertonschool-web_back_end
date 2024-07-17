export default function appendToEachArrayValue(array, appendString) {
    for (let value of array) {
      const newValue = appendString + value;
      array.push(newValue);
    }
    return array.slice();
  }
