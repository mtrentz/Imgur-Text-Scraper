package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
)

func Communicate(imageName string) {
	// Create a json with the key 'msg' and the value of the imageName, that will be saved in /imgs/
	var jsonStr = []byte(fmt.Sprintf(`{"msg":"%s"}`, imageName))

	// Finding API URL
	// If ran in docker-compose, ip is http://analyser:8001, else its localhost
	var url string

	serviceName, isSet := os.LookupEnv("API_SERVICE_NAME")
	if isSet {
		url = fmt.Sprintf("http://%s:8001", serviceName)
	} else {
		url = "http://localhost:8001"
	}

	// POST
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
	if err != nil {
		fmt.Println("NewRequest error: ", err)
		return
	}
	req.Header.Set("X-Custom-Header", "Random String")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("HttpClient error: ", err)
		return
	}
	defer resp.Body.Close()

	// fmt.Println("response Status:", resp.Status)

}
