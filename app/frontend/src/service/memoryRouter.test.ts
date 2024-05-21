import { describe, expect, summary } from "../utils/unittest";
import { addRouterPositionInMemory } from "./memoryRouter";

describe("memoryRouter: addRouterPosition in memory forward", () => {
    const stack = ["home", "about", "contact"];
    const route = "about";
    const newStack = addRouterPositionInMemory(stack, route, "forward");
    expect(newStack).match(["home", "contact", "about"]);
});

describe("memoryRouter: addRouterPosition in memory backwards", () => {
    const stack = ["home", "about", "contact"];
    const route = "about";
    const newStack = addRouterPositionInMemory(stack, route, "back");
    expect(newStack).match(["home", "about"]);
});

summary();

export { };
