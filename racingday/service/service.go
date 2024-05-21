package service

import "net/http"

type HttpService struct {
	Get func(string) (*http.Response, error)
}
type Service struct {
	Http HttpService
}

func NewService(get func(string) (*http.Response, error)) Service {
	return Service{
		Http: HttpService{Get: get},
	}
}
