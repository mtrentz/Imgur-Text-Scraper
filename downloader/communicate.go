package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
)

func Communicate(imageName string) {
	// Create a json with the key 'msg' and the value of the imageName, that will be saved in /imgs/
	var jsonStr = []byte(fmt.Sprintf(`{"msg":"%s"}`, imageName))

	// POST
	// url := "http://testserver:8001"
	url := "http://localhost:8001"
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
	if err != nil {
		panic(err)
	}
	req.Header.Set("X-Custom-Header", "Random String")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))

}
