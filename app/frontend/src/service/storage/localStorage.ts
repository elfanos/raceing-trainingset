/**
 * Check if key it already in use if so throw error
 */
export const addWindowStorageToSet = <T extends any>(key: string) => {
  window.localStorage.getItem(key) ?? window.localStorage.setItem(key, "[]");
  return new Map<string, T>(
    JSON.parse(window.localStorage.getItem(key) ?? "[]"),
  );
};

const customLocalStorage = <T extends any>(key: string) => {
  const storage = addWindowStorageToSet<T>(key);
  return {
    get: (key: string) => storage.get(key),
    set: (key: string, value: T) => {
      storage.set(key, value);
      localStorage.setItem(key, JSON.stringify(Array.from(storage)));
    },
    clear: () => storage.clear(),
  };
};

export default customLocalStorage;
