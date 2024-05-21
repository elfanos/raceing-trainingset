package selector_test

import (
	"fmt"
	"reflect"
	"testing"

	"racingday/game"
	"racingday/racinginfo"
	"racingday/racinginfo/selector"
)

func TestSelector(t *testing.T) {

	mockData := racinginfo.RacingInfo{
		Date: "2023-05-18",
		Games: game.Games{
			V75: []game.Game{
				{ID: "game1", Status: "scheduled"},
				{ID: "game2", Status: "completed"},
			},
			V65: []game.Game{
				{ID: "game3", Status: "ongoing"},
				{ID: "game4", Status: "scheduled"},
			},
			V5: []game.Game{
				{ID: "game5", Status: "completed"},
				{ID: "game6", Status: "ongoing"},
			},
			V4: []game.Game{
				{ID: "game7", Status: "scheduled"},
				{ID: "game8", Status: "completed"},
			},
			V3: []game.Game{
				{ID: "game9", Status: "ongoing"},
				{ID: "game10", Status: "scheduled"},
			},
			DD: []game.Game{
				{ID: "game11", Status: "completed"},
				{ID: "game12", Status: "ongoing"},
			},
			LD: []game.Game{
				{ID: "game13", Status: "scheduled"},
				{ID: "game14", Status: "completed"},
			},
		},
	}

	raceSelectors := selector.NewRacingInfoSelector(&mockData)

	gameIds := raceSelectors.SelectGameIdsFromRacingInfo()

	expected := []string{
		"game1",
		"game2",
		"game3",
		"game4",
		"game5",
		"game6",
		"game7",
		"game8",
		"game9",
		"game10",
		"game11",
		"game12",
		"game13",
		"game14",
	}
	if !reflect.DeepEqual(gameIds, expected) {
		fmt.Println("Expected: ", expected)
		fmt.Println("Actual: ", gameIds)
		t.Fail()
	}

}
