// src/App.tsx
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Container,
  Paper,
  Button,
  Stack
} from "@mui/material";
import { Link as RouterLink, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import AppRouter from "./router";
import { roleStore } from "./config/role";


interface NavItem {
  labelKey: string;
  path: string;
}

const navItems: NavItem[] = [
  { labelKey: "nav.offers", path: "/offers" },
  { labelKey: "nav.candidates", path: "/candidates" },
  { labelKey: "nav.roles", path: "/roles" },
  { labelKey: "nav.processes", path: "/processes" },
  { labelKey: "nav.workflow", path: "/workflow" },   // <--- NUEVO
  { labelKey: "nav.settings", path: "/settings" }
];

export default function App() {
  const { t } = useTranslation("common");
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => {
    // Offers es el "home"
    if (path === "/offers") {
      return (
        location.pathname === "/" || location.pathname.startsWith("/offers")
      );
    }
    return location.pathname.startsWith(path);
  };

  const role = roleStore.getRole();
  const visibleNavItems = navItems.filter((item) => {
    if (role === "candidate") return ["/candidates", "/settings"].includes(item.path);
    if (role === "company") return ["/offers", "/settings"].includes(item.path);
    return true; // recruiter y admin ven todo
  });


  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
      <AppBar position="static" color="primary" elevation={1}>
        <Toolbar>
          <Typography
            variant="h6"
            sx={{ fontWeight: 600, cursor: "pointer" }}
            onClick={() => navigate("/offers")}
          >
            {t("app.title")}
          </Typography>

          <Stack direction="row" spacing={1} sx={{ ml: 4 }}>
            {visibleNavItems.map((item) => {
              const active = isActive(item.path);
              return (
                <Button
                  key={item.path}
                  component={RouterLink}
                  to={item.path}
                  size="small"
                  sx={{
                    textTransform: "none",
                    borderRadius: 2,
                    px: 2,
                    color: active
                      ? "primary.contrastText"
                      : "rgba(255,255,255,0.85)",
                    backgroundColor: active
                      ? "rgba(255,255,255,0.18)"
                      : "transparent",
                    "&:hover": {
                      backgroundColor: "rgba(255,255,255,0.24)"
                    }
                  }}
                >
                  {t(item.labelKey)}
                </Button>
              );
            })}
          </Stack>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 4 }}>
        <Paper sx={{ p: 3 }} elevation={3}>
          <AppRouter />
        </Paper>
      </Container>
    </Box>
  );
}
