package api_test

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	horseAPI "horse-utils/api"

	"racingday/api"
	"racingday/types"
)

func TestFetchRacingInfo(t *testing.T) {

	// Create a sample RacingDay data
	testData := []types.Game{
		{
			ID:                 "V75_2024-05-11_27_5",
			Status:             "results",
			StartTime:          "hola",
			ScheduledStartTime: "hola",
			Tracks:             []int{27},
			Races:              []string{"2024-05-11_27_5"},
			JackpotAmount:      18609579,
			EstimatedJackpot:   44000000,
			AddOns:             []string{"boost"},
			ReturnToPlayer:     65,
			NewBettingSystem:   true,
		},
	}

	// Start a local HTTP server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(testData)
	}))
	defer server.Close()
	// Use server.URL which has the address of the started server
	date := "2024-05-11"
	fmt.Println(server.URL)

	url := fmt.Sprintf("%s/services/racinginfo/v1/api/calendar/day", server.URL)

	cool := url + "/%s"

	endpoints := types.Endpoints{
		RacingInfo: cool,
	}
	service := types.NewRacingInfoService(server.Client().Get)
	app := api.NewRacingDayAPI(endpoints, service)

	info, err := app.FetchRacingInfo(date)

	jsonString, err := horseAPI.JSONPretty(info)
	fmt.Println(jsonString)
	fmt.Println(err)
	fmt.Println(info)
}
