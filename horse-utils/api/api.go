package api

import (
	"encoding/json"
	"fmt"
)

func JSONPretty(T any) (string, error) {
	prettyJSON, err := json.MarshalIndent(T, "", "    ") // Indent with four spaces
	if err != nil {
		return "", fmt.Errorf("Error marshalling JSON: %w", err)
	}
	return string(prettyJSON), nil
}
