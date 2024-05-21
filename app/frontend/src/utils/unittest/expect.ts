import match from "./match";
import { addToSummary } from "./summary";

export default function expect<T extends any>(value: T) {
    return {
        match: <T extends any>(comparer: T) => {
            const matched = match(value, comparer);
            addToSummary(matched);
            if (matched.ok) {
                console.log("PASSED: ", matched.message);
                return;
            }
            console.log("FAILED: ", matched.message);
        },
    };
}
