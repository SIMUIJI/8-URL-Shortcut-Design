package main

import (
	"api/go_api/config"
	"api/go_api/db"
	"fmt"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"net"
	"net/http"
	"os"
	"strings"
)

//env GOOS=linux GOARCH=arm64 go build -o main
//env GOOS=linux GOARCH=amd64 go build -o main
//set GOOS=linux& set GOARCH=amd64& go build -o main
//cp main ../api1/
//cp main ../api2/

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	ip := myIP()
	ips := strings.Join(ip, " ")

	config.DatabaseInit()
	config.CacheInit()
	//gorm := config.DB()
	//
	//dbGorm, err := gorm.DB()
	//if err != nil {
	//	panic(err)
	//}

	// Route => handler
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, ips)
	})
	urlRoute := e.Group("/api/v1")
	urlRoute.POST("/shorten", db.CreateUrl)
	urlRoute.GET("/:short_url", db.GetUrl)
	//urlRoute.PUT("/:long_url", db.UpdateUrl)
	//urlRoute.DELETE("/:long_url", db.DeleteUrl)

	// Start server
	e.Logger.Fatal(e.Start(":1323"))
}

func myIP() []string {
	myIp := []string{}
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	fmt.Println("Local IP addresses:")
	for _, addr := range addrs {
		// IPv4 주소만 필터링
		if ipNet, ok := addr.(*net.IPNet); ok && !ipNet.IP.IsLoopback() {
			if ipNet.IP.To4() != nil {
				fmt.Println(ipNet.IP.String())
				myIp = append(myIp, ipNet.IP.String())
			}
		}
	}
	return myIp
}
