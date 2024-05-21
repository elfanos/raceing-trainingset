package driver

import "racingday/common"

type DriverStats struct {
	Years map[string]common.Stats `json:"years"`
}

type Driver struct {
	ID         int              `json:"id"`
	FirstName  string           `json:"firstName"`
	LastName   string           `json:"lastName"`
	ShortName  string           `json:"shortName"`
	Location   string           `json:"location"`
	Birth      int              `json:"birth"`
	HomeTrack  common.HomeTrack `json:"homeTrack"`
	License    string           `json:"license"`
	Silks      string           `json:"silks"`
	Statistics DriverStats      `json:"statistics"`
}
