package horse

import (
	"racingday/common"
	"racingday/trainer"
)

type Owner struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}
type Breeder struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type Record struct {
	Code        string      `json:"code"`
	StartMethod string      `json:"startMethod"`
	Distance    string      `json:"distance"`
	Time        common.Time `json:"time"`
}

type Font struct {
	HasShoe bool `json:"hasShoe"`
	Changed bool `json:"changed"`
}

type Back struct {
	HasShoe bool `json:"hasShoe"`
	Changed bool `json:"changed"`
}

type Shoes struct {
	Reported bool `json:"reported"`
	Font     Font `json:"font"`
	Back     Back `json:"back"`
}

type Type struct {
	Code    string `json:"code"`
	Text    string `json:"text"`
	EngText string `json:"engText"`
	Changed bool   `json:"changed"`
}

type Colour struct {
	Code    string `json:"code"`
	Text    string `json:"text"`
	EngText string `json:"engText"`
	Changed bool   `json:"changed"`
}

type SulkyType struct {
	Code    string `json:"code"`
	Text    string `json:"text"`
	EngText string `json:"engText"`
	Changed bool   `json:"changed"`
}

type Sulky struct {
	Reported bool      `json:"reported"`
	Type     SulkyType `json:"type"`
	Colour   Colour    `json:"colour"`
}

type Parent struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Nationality string `json:"nationality"`
}

type Pedigree struct {
	Father      Parent `json:"father"`
	Mother      Parent `json:"mother"`
	GrandFather Parent `json:"grandfather"`
}

type LifeStats struct {
	Starts           int              `json:"starts"`
	Earnings         int64            `json:"earnings"`
	Placement        common.Placement `json:"placement"`
	Records          []Record         `json:"records"`
	WinPercentage    int              `json:"winPercentage"`
	PlacePercentage  int              `json:"placePercentage"`
	EarningsPerStart int              `json:"earningsPerStart"`
	StartPoints      int              `json:"startPoints"`
}

type LastFiveStarts struct {
	AverageOdds int `json:"averageOdds"`
}

type HorseStats struct {
	Years          map[string]common.Stats `json:"years"`
	Life           LifeStats               `json:"life"`
	LastFiveStarts LastFiveStarts          `json:"lastFiveStarts"`
}

type Horse struct {
	ID         int              `json:"id"`
	Name       string           `json:"name"`
	Age        int              `json:"age"`
	Sex        string           `json:"sex"`
	Record     Record           `json:"record"`
	Trainer    trainer.Trainer  `json:"trainer"`
	Shoes      Shoes            `json:"shoes"`
	Sulky      Sulky            `json:"sulky"`
	Money      int              `json:"money"`
	Color      string           `json:"color"`
	HomeTrack  common.HomeTrack `json:"homeTrack"`
	Owner      Owner            `json:"owner"`
	Breeder    Breeder          `json:"breeder"`
	Statistics HorseStats       `json:"statistics"`
	Pedigree   Pedigree         `json:"pedigree"`
}
