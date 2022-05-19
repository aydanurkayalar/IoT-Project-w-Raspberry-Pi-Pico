package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

func main() {

	var button int
	button = 1

	for {

		fmt.Printf("enter 0 or 1\n")
		fmt.Scanf("%d\n", &button)
		time.Sleep(3 * time.Second)
		fmt.Printf("BTN: %v\n", button)

		if button == 1 {
			setButtonStatus("1")

			time.Sleep(2 * time.Second)

		} else if button == 0 {

			setButtonStatus("0")
			time.Sleep(2 * time.Second)
		}

	}

}

func setButtonStatus(status string) {
	resp, err := http.Get("https://api.thingspeak.com/update?api_key=ZUPIM2V5K8RVN6AJ&field2=" + status)
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(body))
}
