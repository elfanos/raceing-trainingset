package result

import "racingday/common"

type Result struct {
	Place        int         `json:"place"`
	FinishOrder  int         `json:"finishOrder"`
	KmTime       common.Time `json:"kmTime"`
	PrizeMoney   int         `json:"prizeMoney"`
	FinalOdds    float64     `json:"finalOdds"`
	StartNumber  int         `json:"startNumber"`
	Galloped     bool        `json:"galloped"`
	Disqualified bool        `json:"disqualified"`
}
