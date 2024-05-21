package game

type Game struct {
	ID                 string   `json:"id"`
	Status             string   `json:"status"`
	StartTime          string   `json:"startTime"`
	ScheduledStartTime string   `json:"scheduledStartTime"`
	Tracks             []int    `json:"tracks"`
	Races              []string `json:"races"`
	JackpotAmount      int      `json:"jackpotAmount"`
	EstimatedJackpot   int      `json:"estimatedJackpot"`
	AddOns             []string `json:"addOns"`
	ReturnToPlayer     int      `json:"returnToPlayer"`
	NewBettingSystem   bool     `json:"newBettingSystem"`
}

type Games struct {
	V75 []Game `json:"V75"`
	V65 []Game `json:"V65"`
	V5  []Game `json:"V5"`
	V4  []Game `json:"V4"`
	V3  []Game `json:"V3"`
	DD  []Game `json:"dd"`
	LD  []Game `json:"ld"`
}
