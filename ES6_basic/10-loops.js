export default function appendToEachArrayValue(array, appendString) {
  for (const value of array) {
    const newValue = appendString + value;
    array.push(newValue);
  }
  return array.slice();
}
