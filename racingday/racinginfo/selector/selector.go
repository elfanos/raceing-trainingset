package selector

import (
	"reflect"

	"racingday/game"
	"racingday/racinginfo"
)

type RacingInfoSelector struct {
	data *racinginfo.RacingInfo
}

func NewRacingInfoSelector(r *racinginfo.RacingInfo) RacingInfoSelector {
	return RacingInfoSelector{
		data: r,
	}
}

func (r RacingInfoSelector) SelectGameIdsFromRacingInfo() []string {

	var gameIds []string
	racingDataReflection := reflect.ValueOf(*r.data)
	games := racingDataReflection.FieldByName("Games").Interface().(game.Games)

	gamesReflection := reflect.ValueOf(games)

	for i := 0; i < gamesReflection.NumField(); i++ {
		gameArrayReflection := gamesReflection.Field(i)

		for j := 0; j < gameArrayReflection.Len(); j++ {
			gameIds = append(gameIds, gameArrayReflection.Index(j).Interface().(game.Game).ID)
		}
	}

	return gameIds
}
