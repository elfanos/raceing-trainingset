package track

type TrackRace struct {
	ID        string `json:"id"`
	Status    string `json:"status"`
	StartTime string `json:"startTime"`
	Number    int    `json:"number"`
}

type GameTrack struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Condition   string `json:"condition"`
	CountryCode string `json:"countryCode"`
}

type Track struct {
	ID              int         `json:"id"`
	Name            string      `json:"name"`
	BiggestGameType string      `json:"biggestGameType"`
	CountryCode     string      `json:"countryCode"`
	TrackChanged    bool        `json:"trackChanged"`
	Sport           string      `json:"sport"`
	Races           []TrackRace `json:"races"`
}
