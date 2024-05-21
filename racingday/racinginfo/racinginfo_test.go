package racinginfo_test

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	horseAPI "horse-utils/api"

	"racingday/api"
	"racingday/racinginfo"
	"racingday/service"
	"racingday/types"
)

func TestFetchRacingInfo(t *testing.T) {

	data, err := os.Open("./mocks/racinginfo.json")
	if err != nil {
		t.Fatalf("Error reading JSON file: %v", err)
	}
	defer data.Close()

	testData, err := io.ReadAll(data)

	if err != nil {
		t.Fatalf("Error reading JSON file: %v", err)
	}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write(testData)
	}))

	defer server.Close()

	// Use server.URL which has the address of the started server
	date := "2024-05-11"
	fmt.Println(server.URL)
	//
	url := fmt.Sprintf("%s/services/racinginfo/v1/api/calendar/day", server.URL)
	//
	endpoint := url + "/%s"

	service := service.NewService(server.Client().Get)
	apiController := api.APIController{
		Endpoints: types.Endpoints{
			RacingInfo: endpoint,
		},
		Service: service,
	}

	info, err := racinginfo.NewRaceInfoHandler(apiController).FetchRacingInfo(date)

	if err != nil {
		t.Fatalf("Error fetching racing info: %v", err)
	}

	jsonString, _ := horseAPI.JSONPretty(info)
	fmt.Println(jsonString)
}

func TestFetchRacingInfoGame(t *testing.T) {

	data, err := os.Open("./mocks/racinginfogame.json")
	if err != nil {
		t.Fatalf("Error reading JSON file: %v", err)
	}
	defer data.Close()

	testData, err := io.ReadAll(data)

	if err != nil {
		t.Fatalf("Error reading JSON file: %v", err)
	}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write(testData)
	}))

	defer server.Close()

	// Use server.URL which has the address of the started server
	id := "V75_2024-05-11_27_5"
	fmt.Println(server.URL)
	//
	url := fmt.Sprintf("%s/services/racinginfo/v1/api/calendar/day", server.URL)
	//
	endpoint := url + "/%s"

	service := service.NewService(server.Client().Get)

	racingInfoGameUrl := "https://www.atg.se/services/racinginfo/v1/api/games"

	racingInfoGameEndpoint := racingInfoGameUrl + "/%s"

	apiController := api.APIController{
		Endpoints: types.Endpoints{
			RacingInfo:     endpoint,
			RacingInfoGame: racingInfoGameEndpoint,
		},
		Service: service,
	}

	info, err := racinginfo.NewRaceInfoHandler(apiController).FetchRacingInfoGame(id)

	if err != nil {
		t.Fatalf("Error fetching racing info: %v", err)
	}

	jsonString, _ := horseAPI.JSONPretty(info)
	fmt.Println(jsonString)
}
