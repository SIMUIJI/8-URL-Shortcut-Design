package main

import (
	"api/go_api/cmd"
	"api/go_api/cmd/myip"
	_ "api/go_api/config"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
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

	// Route => handler
	e.GET("/", myip.MyIp)
	cmd.UrlRoute(e)

	// Start server
	e.Logger.Fatal(e.Start(":1323"))
}
