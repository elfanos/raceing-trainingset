package main

import (
	"context"
	"fmt"
	"net/http"

	horseAPI "horse-utils/api"
	"racingday/api"
	"racingday/racinginfo"
	"racingday/service"
	"racingday/types"
)

// App struct
type App struct {
	ctx               context.Context
	racingInfoHandler racinginfo.RacingInfoHandler
}

// NewApp creates a new App application struct
func NewApp() *App {

	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx

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
	a.racingInfoHandler = racingInfo
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, It's show time!", name)
}
func (a *App) RacingInfo(date string) string {

	cool := "2024-05-11"
	fetchedRacingInfo, err := a.racingInfoHandler.FetchRacingInfo(cool)
	if err != nil {
		fmt.Printf("Error fetching racing info: %v", err)
	}
	jsonString, _ := horseAPI.JSONPretty(fetchedRacingInfo)
	fmt.Println(jsonString)
	return jsonString
}
