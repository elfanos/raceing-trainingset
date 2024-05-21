type Store = {
  racingInfo: null | string;
};
const AppStore: Store = {
  racingInfo: null,
};
const store = new Proxy(AppStore, {
  set: (store: Store, prop: keyof Store, value: any) => {
    if (prop === "racingInfo") {
      store[prop] = value;
      window.dispatchEvent(new Event("racingInfo"));
    }
    return true;
  },
});

export default store;
