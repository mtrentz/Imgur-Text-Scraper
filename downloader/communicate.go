package main

import (
	"bytes"
	"fmt"
	"net/http"
)

func Communicate(imageName string) {
	// Create a json with the key 'msg' and the value of the imageName, that will be saved in /imgs/
	var jsonStr = []byte(fmt.Sprintf(`{"msg":"%s"}`, imageName))

	// POST
	url := "http://analyser:8001"
	// url := "http://localhost:8001"
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
	if err != nil {
		fmt.Println(err)
	}
	req.Header.Set("X-Custom-Header", "Random String")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)

}
