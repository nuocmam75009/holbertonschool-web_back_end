export default function updateUniqueItems(itemsMap) {
  if (!(itemsMap instanceof Map)) {
    throw new Error('Cannot process');
  }
  itemsMap.forEach((value, key) => {
	  if (value === 1) {
		itemsMap.set(key, 100);
	  }
  });
  return itemsMap;
}
