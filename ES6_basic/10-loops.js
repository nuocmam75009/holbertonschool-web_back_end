export default function appendToEachArrayValue(array, appendString) {
    for (let value of array) {
        const array2 = value + appendString;
        array.push(array2);
    }
    return array.slice();
}