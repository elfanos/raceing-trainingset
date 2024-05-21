import { UnitTestContract } from "./types";

const testSummary = {
    numberOfTests: 0,
    numberOfPassed: 0,
    numberOfFailed: 0,
};

export function addToSummary(result: UnitTestContract) {
    testSummary.numberOfTests++;
    if (result.ok) {
        testSummary.numberOfPassed++;
        return;
    }
    testSummary.numberOfFailed++;
}
export default function summary() {
    console.log("Tests: ", testSummary.numberOfTests);
    console.log("Passed: ", testSummary.numberOfPassed);
    console.log("Failed: ", testSummary.numberOfFailed);
}
