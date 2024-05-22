package app

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"

	"racingday/api"
	"racingday/racinginfo"
	"racingday/racinginfo/selector"
	"racingday/service"
	"racingday/types"
)

func App() {
	serverUrl := "https://www.atg.se"
	serverEndpoint := "services/racinginfo/v1/api"

	// racing info endpoint

	racingInfoUrl := fmt.Sprintf("%s/%s/calendar/day", serverUrl, serverEndpoint)
	racingInfoEndpoint := racingInfoUrl + "/%s"

	// racing info game endpoint
	racingInfoGameUrl := fmt.Sprintf("%s/%s/games", serverUrl, serverEndpoint)
	racingInfoGameEndpoint := racingInfoGameUrl + "/%s"

	service := service.NewService(http.Get)

	apiController := api.APIController{
		Endpoints: types.Endpoints{
			RacingInfo:     racingInfoEndpoint,
			RacingInfoGame: racingInfoGameEndpoint,
		},
		Service: service,
	}

	racingInfo := racinginfo.NewRaceInfoHandler(apiController)
	fmt.Println(racingInfo)

	date := "2024-05-18"
	fetchedRacingInfo, err := racingInfo.FetchRacingInfo(date)
	if err != nil {
		fmt.Printf("Error fetching racing info: %v", err)
	}

	racingInfoSelector := selector.NewRacingInfoSelector(fetchedRacingInfo)
	gameIds := racingInfoSelector.SelectGameIdsFromRacingInfo()

	var wg sync.WaitGroup
	results := make([]*racinginfo.RacingInfoGame, len(gameIds))
	error := make([]error, len(gameIds))
	for i, id := range gameIds {
		wg.Add(1)
		go func(i int, id string) {
			defer wg.Done()
			info, err := racingInfo.FetchRacingInfoGame(id)
			if err != nil {
				error[i] = err
				return
			}
			results[i] = info

		}(i, id)
	}
	wg.Wait()

	for i, err := range error {
		if err != nil {
			fmt.Printf("Error fetching racing info: %v", err)
		} else {

			fmt.Println("Fetched info from this game ID %s, with this info %w", gameIds[i], results[i])
		}
	}

	if err != nil {
		fmt.Printf("Error fetching racing info: %v", err)
	}

	file, err := os.Create("results.json")

	if err != nil {
		fmt.Printf("Error creating JSON file: %v\n", err)
		return
	}
	defer file.Close()

	// Serialize results to JSON
	jsonData, err := json.MarshalIndent(results, "", "  ")
	if err != nil {
		fmt.Printf("Error marshalling results to JSON: %v\n", err)
		return
	}

	_, err = file.Write(jsonData)
	if err != nil {
		fmt.Printf("Error writing to JSON file: %v\n", err)
		return
	}

	fmt.Println("Results written to results.json")
}
func check(e error) {
	if e != nil {
		panic(e)
	}
}
