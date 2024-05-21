package start

import (
	"racingday/common"
	"racingday/driver"
	"racingday/horse"
)

type StartResult struct {
	Place        int         `json:"place"`
	FinishOrder  int         `json:"finishOrder"`
	KmTime       common.Time `json:"kmTime"`
	PrizeMoney   int         `json:"prizeMoney"`
	FinalOdds    float64     `json:"finalOdds"`
	StartNumber  int         `json:"startNumber"`
	Galloped     bool        `json:"galloped"`
	Disqualified bool        `json:"disqualified"`
}

type Start struct {
	ID           string        `json:"id"`
	Number       int           `json:"number"`
	PostPosition int           `json:"postPosition"`
	Distance     int           `json:"distance"`
	Horse        horse.Horse   `json:"horse"`
	Driver       driver.Driver `json:"driver"`
	Result       StartResult   `json:"result"`
	Scratched    bool          `json:"scratched"`
}
