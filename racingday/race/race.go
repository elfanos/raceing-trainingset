package race

import (
	"racingday/start"
	"racingday/track"
)

type Result struct {
	VictoryMargin string `json:"victoryMargin"`
	Scratchings   []int  `json:"scratchings"`
}

type GameRace struct {
	ID                 string          `json:"id"`
	Name               string          `json:"name"`
	Date               string          `json:"date"`
	Number             int             `json:"number"`
	Distance           int             `json:"distance"`
	StartMethod        string          `json:"startMethod"`
	StartTime          string          `json:"startTime"`
	ScheduledStartTime string          `json:"scheduledStartTime"`
	Prize              string          `json:"prize"`
	Terms              []string        `json:"terms"`
	Sport              string          `json:"sport"`
	Track              track.GameTrack `json:"track"`
	Result             Result          `json:"result"`
	Status             string          `json:"status"`
	MediaID            string          `json:"mediaId"`
	Starts             []start.Start   `json:"starts"`
}
