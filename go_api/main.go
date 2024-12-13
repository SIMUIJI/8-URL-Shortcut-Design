package main

import (
	"api/cmd"
	"api/cmd/myip"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

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
