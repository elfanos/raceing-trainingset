package racinginfo

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"racingday/api"
	"racingday/game"
	"racingday/race"
	"racingday/track"
)

type RacingInfo struct {
	Date   string        `json:"date"`
	Tracks []track.Track `json:"tracks"`
	Games  game.Games    `json:"games"`
}

type RacingInfoGame struct {
	ID               string          `json:"id"`
	Status           string          `json:"status"`
	Races            []race.GameRace `json:"races"`
	NewBettingSystem bool            `json:"newBettingSystem"`
	Type             string          `json:"type"`
}

type RacingInfoHandler struct {
	apiController api.APIController
}

func NewRaceInfoHandler(apiController api.APIController) RacingInfoHandler {
	return RacingInfoHandler{
		apiController,
	}
}

// I want to fetch only the game ids inside games:{
// 	"V75": [{id:""}]

func (raceInfoHandler RacingInfoHandler) FetchRacingInfoGameIds(date string) ([]string, error) {
	raceinfo, err := raceInfoHandler.FetchRacingInfo(date)

	if err != nil {
		return nil, fmt.Errorf("error %v", err)
	}

	var gameIds []string
	for _, game := range raceinfo.Games.V75 {
		gameIds = append(gameIds, game.ID)
	}

	return gameIds, nil
}
func (raceInfoHandler RacingInfoHandler) FetchRacingInfo(date string) (*RacingInfo, error) {
	url := fmt.Sprintf(raceInfoHandler.apiController.Endpoints.RacingInfo, date)

	resp, err := raceInfoHandler.apiController.Service.Http.Get(url)

	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {

		return nil, fmt.Errorf("server returned non-200 status code: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)

	if err != nil {
		return nil, err
	}

	var info RacingInfo
	if err = json.Unmarshal(body, &info); err != nil {
		fmt.Println("error", err)
		return nil, err
	}

	return &info, nil

}

func (raceInfoHandler RacingInfoHandler) FetchRacingInfoGame(id string) (*RacingInfoGame, error) {

	url := fmt.Sprintf(raceInfoHandler.apiController.Endpoints.RacingInfoGame, id)

	resp, err := raceInfoHandler.apiController.Service.Http.Get(url)

	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {

		return nil, fmt.Errorf("server returned non-200 status code: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)

	if err != nil {
		return nil, err
	}

	var info RacingInfoGame
	if err = json.Unmarshal(body, &info); err != nil {
		fmt.Println("error", err)
		return nil, err
	}

	return &info, nil

}
