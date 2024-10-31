package myip

import (
	"api/go_api/internal"
	"github.com/labstack/echo/v4"
	"net/http"
	"strings"
)

func MyIp(c echo.Context) error {
	ip := internal.MyIP()
	ips := strings.Join(ip, " ")

	return c.String(http.StatusOK, ips)
}
