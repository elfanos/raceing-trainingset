package api

import (
	"racingday/service"
	"racingday/types"
)

type APIController struct {
	Endpoints types.Endpoints
	Service   service.Service
}

func NewAPIController(endpoints types.Endpoints, service service.Service) APIController {
	return APIController{
		Endpoints: endpoints,
		Service:   service,
	}
}
