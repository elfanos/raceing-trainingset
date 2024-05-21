package common

type Placement struct {
	First  int `json:"1"`
	Second int `json:"2"`
	Third  int `json:"3"`
}

type Stats struct {
	Starts        int       `json:"starts"`
	Earnings      int64     `json:"earnings"`
	Placement     Placement `json:"placement"`
	WinPercentage int       `json:"winPercentage"`
}

type HomeTrack struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type Time struct {
	Minutes int `json:"minutes"`
	Seconds int `json:"seconds"`
	Tenths  int `json:"tenths"`
}
