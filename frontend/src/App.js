import React, { useState, useEffect } from "react";
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Alert,
  Tabs,
  Tab,
  useTheme,
  alpha,
  IconButton,
  CssBaseline,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Stack,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import {
  UploadFile,
  Add as AddIcon,
  Delete as DeleteIcon,
  DarkMode,
  LightMode,
} from "@mui/icons-material";
import axios from "axios";

// Predefined requirements for different roles
const jobRoleRequirements = {
  developer: [
    // Sprachkenntnisse
    "Sehr gute Deutschkenntnisse (C1, Sehr Gut, Muttersprache, fließend, verhandlungssicher)",
    // MS Office
    "Microsoft Office Kenntnisse",
    // Prozessmodellierung
    "Prozessmodellierung",
    // SAP Core und Basis
    "SAP Core und Basis Kenntnisse",
    // ECC Systeme
    "SAP IS-U Kenntnisse",
    "IDEX-Framework Erfahrung",
    // S/4 Systeme
    "S/4 Utilities Expertise",
    "MaCo Cloud (APE) /UCOM Kenntnisse",
    // ECC und S/4 Prozesse
    "Stammdaten/Datenmodelle und Messkonzepte",
    "Geräteverwaltung",
    "EDM Expertise",
    "Abrechnungs- und Fakturierungsprozesse",
    "FI-CA Kenntnisse",
    "MOS-Billing inkl. MaKo",
    "MeMi inkl. MaKo",
    "EEG Billing",
    // SAP Technologie und Development Framework
    "SAP-Transportverwaltung",
    "RAP - Rest Application Programming Model",
    "CAP - Cloud Application Programming Model",
    "BTP (Business Technology Platform) Kenntnisse",
    "Fiori und Core Data Views (CDS)",
    "ABAP, ABAP OO",
    "BTP / Integration Platform / CPI",
    // NonSAP Technologies
    "JavaScript, NodeJS, bower",
    "Python, Jupyter Notebook, Pandas",
    "HTML, CSS",
    "SOAP Webservices",
    "REST/OData",
    "SOA",
    "Solution Design/-Architektur",
    "Software-Architektur",
    "Software-Lifecycle",
    "CI/CD",
    "SQL Datenbanken",
    // Modellierung
    "BPMN Kenntnisse",
    "UML Kenntnisse",
    // Requirements Engineering
    "Fachkonzepterstellung",
    "Erstellung Technisches Konzept",
    "Anforderungsdefinition/-management",
    "Lastenheft- und Pflichtenhefterstellung",
    // Projektmanagement
    "Scrum und Kanban",
    "Trainingsdesign und -durchführung",
    "Erstellung und Pflege von Projekt-, Zeit-, Ressourcenplänen",
    // Energiewirtschaft Allgemein
    "Kundenservice in der Energiewirtschaft",
    "Messdatenmanagement",
    "Marktkommunikation",
    "Messkonzepte und komplexe Messstellen",
    "Wechselprozesse (GPKE, GeLi Gas, WiM)",
    "Energiemengenbilanzierung/EDM (MaBiS/GaBi Gas)",
    "EnWG Kenntnisse",
    // Energiewirtschaft Netz
    "Netzabrechnung",
    "Einspeiserabrechnung",
    // Energiewirtschaft Lieferant
    "CRM in der Energiewirtschaft",
    "Rechnungseingangsprüfung",
    "Endkundenabrechnung",
    // Energiewirtschaft MSB
    "Smart Meter",
    "GDEW, MsbG Kenntnisse",
    "MDM - Meter Data Management",
    "Workforcemanagement und Ablesung",
    // Ausbildung
    "Hochschulabschluss oder vergleichbare Qualifikation",
    // Soft Skills
    "Hohes Engagement",
    "Ausgeprägte Teamfähigkeit",
    "Starke Kundenorientierung",
    // Standort
    "Standort: Bevorzugt Region Mannheim, Rhein-Neckar-Region und alles im Umkreis, auch Düsseldorf/Wuppertal oder Thüringen",
    // Ähnliche Unternehmen
    "Erfahrung in vergleichbaren Unternehmen (z.B. Convista, koenig.solutions, incept4, cronos, INTENSE AG, Hochfrequenz, DSC, Power Reply, NEA Gruppe, cerebricks, ENERGY4U, Nexus Nova, DEMANDO, adesso orange)",
  ],
  consultant: [
    // Ausbildung und Sprachen
    "Hochschulabschluss oder vergleichbare Qualifikation",
    "Sehr gute Deutschkenntnisse (C1, Sehr Gut, Muttersprache, fließend, verhandlungssicher)",
    // MS Office
    "Microsoft Office Kenntnisse",
    // Prozessmodellierung
    "Erfahrung mit Prozessmodellierung (z.B. Camunda, Signavio)",
    "BPMN und UML Kenntnisse",
    // SAP Core und Basis
    "SAP Core und Basis Kenntnisse",
    // ECC
    "SAP IS-U Erfahrung",
    "IDEX-Framework Kenntnisse",
    "IM4G Erfahrung",
    // S/4
    "S/4 Utilities Expertise",
    "MaCo Cloud (APE) /UCOM Kenntnisse",
    // ECC und S/4 Prozesse
    "Erfahrung mit Stammdaten/Datenmodellen und Messkonzepten",
    "Kenntnisse in Geräteverwaltung",
    "EDM Expertise",
    "Abrechnungs- und Fakturierungsprozesse",
    "FI-CA Kenntnisse",
    "MOS-Billing inkl. MaKo",
    "MeMi inkl. MaKo",
    "EEG Billing",
    // SAP Technologie
    "BTP (Business Technology Platform)",
    "Fiori und Core Data Views (CDS)",
    "ABAP, ABAP OO",
    "BTP / Integration Platform / CPI",
    // NonSAP
    "HTML, CSS",
    "REST/OData",
    "SOA",
    "Solution Design/-Architektur",
    "Software-Architektur",
    "Software-Lifecycle",
    "SQL Datenbanken",
    // Prozessmanagement
    "Prozessanalyse und Prozessbeschreibung",
    "Testen, Testfälle, Testkoordination",
    // Requirements Engineering
    "Fachkonzepterstellung",
    "Erstellung Technisches Konzept",
    "Anforderungsdefinition/-management",
    "Lastenheft- und Pflichtenhefterstellung",
    // Projektmanagement
    "Make or Buy Analyse",
    "Kosten-Nutzen-Bewertung",
    "Scrum und Kanban",
    "Durchführung von fit/gap Workshops",
    "Trainingsdesign und -durchführung",
    "Erstellung und Pflege von Projekt-, Zeit-, Ressourcenplänen",
    // Energiewirtschaft Allgemein
    "Kundenservice in der Energiewirtschaft",
    "Messdatenmanagement",
    "Marktkommunikation",
    "Messkonzepte und komplexe Messstellen",
    "Wechselprozesse (GPKE, GeLi Gas, WiM)",
    "Energiemengenbilanzierung/EDM (MaBiS/GaBi Gas)",
    "EnWG Kenntnisse",
    // Energiewirtschaft Netz
    "Netzabrechnung",
    "Einspeiserabrechnung",
    // Energiewirtschaft Lieferant
    "CRM in der Energiewirtschaft",
    "Rechnungseingangsprüfung",
    "Endkundenabrechnung",
    // Energiewirtschaft MSB
    "Smart Meter",
    "GDEW, MsbG Kenntnisse",
    "MDM - Meter Data Management",
    "Workforcemanagement und Ablesung",
    // Soft Skills
    "Hohes Engagement",
    "Ausgeprägte Teamfähigkeit",
    "Starke Kundenorientierung",
    // Standort
    "Standort: Bevorzugt Region Mannheim, Rhein-Neckar-Region und alles im Umkreis, auch Düsseldorf/Wuppertal oder Thüringen",
    // Ähnliche Unternehmen
    "Erfahrung in vergleichbaren Unternehmen (z.B. Convista, koenig.solutions, incept4, cronos, INTENSE AG, Hochfrequenz, DSC, Power Reply, NEA Gruppe, cerebricks, ENERGY4U, Nexus Nova, DEMANDO, adesso orange)",
  ],
};

// Update the theme configuration
const getDesignTokens = (mode) => ({
  palette: {
    mode,
    primary: {
      main: "#1e8449", // Smaragdgrün als Hauptfarbe
      light: "#27ae60",
      dark: "#145a32",
    },
    secondary: {
      main: "#8e44ad", // Tiefes Lila als Sekundärfarbe
      light: "#9b59b6",
      dark: "#6c3483",
    },
    background: {
      default: mode === "light" ? "#f8f9fa" : "#0a0c0d", // Hintergrundfarbe
      paper: mode === "light" ? "#ffffff" : "#1a1c1e",
    },
    text: {
      primary: mode === "light" ? "#2c3e50" : "#ecf0f1", // Textfarben
      secondary:
        mode === "light" ? "rgba(44, 62, 80, 0.7)" : "rgba(236, 240, 241, 0.7)",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
      letterSpacing: "0.1em",
      background:
        mode === "light"
          ? "linear-gradient(45deg, #1e8449 30%, #8e44ad 90%)"
          : "linear-gradient(45deg, #27ae60 30%, #9b59b6 90%)",
      backgroundClip: "text",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      textShadow: "0 2px 4px rgba(0,0,0,0.1)",
    },
    h6: {
      fontWeight: 500,
      letterSpacing: "0.05em",
      color: mode === "light" ? "#1e8449" : "#27ae60",
    },
    subtitle1: {
      letterSpacing: "0.04em",
    },
    body1: {
      letterSpacing: "0.02em",
    },
  },
  components: {
    MuiContainer: {
      styleOverrides: {
        maxWidthLg: {
          maxWidth: "1440px !important",
          padding: "0 32px",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          backgroundColor: mode === "light" ? "#ffffff" : "#1a1c1e",
          backdropFilter: mode === "light" ? "blur(20px)" : "blur(10px)",
          border: (theme) =>
            `1px solid ${
              theme.palette.mode === "light"
                ? "rgba(30, 132, 73, 0.1)"
                : "rgba(39, 174, 96, 0.1)"
            }`,
          transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
          "&:hover": {
            boxShadow: (theme) =>
              `0 16px 48px ${
                theme.palette.mode === "light"
                  ? "rgba(30, 132, 73, 0.12)"
                  : "rgba(39, 174, 96, 0.12)"
              }`,
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: "none",
          fontWeight: 500,
          letterSpacing: "0.05em",
          padding: "12px 28px",
          transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
          "&:hover": {
            boxShadow: "0 4px 16px rgba(30, 132, 73, 0.2)",
          },
        },
        contained: {
          background:
            mode === "light"
              ? "linear-gradient(45deg, #1e8449 30%, #8e44ad 90%)"
              : "linear-gradient(45deg, #27ae60 30%, #9b59b6 90%)",
          color: "#ffffff",
          boxShadow: "0 4px 16px rgba(30, 132, 73, 0.2)",
          "&:hover": {
            background:
              mode === "light"
                ? "linear-gradient(45deg, #145a32 30%, #6c3483 90%)"
                : "linear-gradient(45deg, #1e8449 30%, #8e44ad 90%)",
            boxShadow: "0 8px 32px rgba(30, 132, 73, 0.3)",
          },
        },
        outlined: {
          borderColor: mode === "light" ? "#1e8449" : "#27ae60",
          borderWidth: "2px",
          color: mode === "light" ? "#1e8449" : "#27ae60",
          "&:hover": {
            borderColor: mode === "light" ? "#27ae60" : "#2ecc71",
            backgroundColor:
              mode === "light"
                ? "rgba(30, 132, 73, 0.08)"
                : "rgba(39, 174, 96, 0.08)",
            boxShadow: "0 4px 16px rgba(30, 132, 73, 0.15)",
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 12,
            transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            "&:hover": {
              boxShadow: "0 4px 16px rgba(30, 132, 73, 0.1)",
            },
            "&.Mui-focused": {
              boxShadow: "0 8px 32px rgba(30, 132, 73, 0.15)",
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
          "&:hover": {
            transform: "translateY(-1px)",
            boxShadow: "0 4px 12px rgba(30, 132, 73, 0.1)",
          },
        },
        outlined: {
          borderWidth: "2px",
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.1)",
        },
      },
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    "none",
    "0 2px 4px rgba(0,0,0,0.05)",
    "0 4px 8px rgba(0,0,0,0.05)",
    "0 8px 16px rgba(0,0,0,0.05)",
    "0 16px 32px rgba(0,0,0,0.05)",
    // ... rest of the shadows array
  ],
});

function JobRoleTab({ value, index, children }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [mode, setMode] = useState("light");
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode)), [mode]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [requirements, setRequirements] = useState("");
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedRole, setSelectedRole] = useState("developer");

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
  };

  const handleRoleChange = (event) => {
    const role = event.target.value;
    setSelectedRole(role);
    setRequirements(jobRoleRequirements[role].join("\n"));
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleRequirementsChange = (event) => {
    setRequirements(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResults(null);
    setLoading(true);

    if (!selectedFile) {
      setError("Bitte eine PDF-Datei auswählen.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    // Encode the requirements as a query parameter
    const apiUrl = `http://localhost:8000/analyze?requirements=${encodeURIComponent(requirements)}&role=${selectedRole}`;

    try {
      const response = await axios.post(apiUrl, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data);
    } catch (err) {
      console.error("Fehler:", err);
      setError("Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container
        maxWidth="lg"
        sx={{
          py: 6,
          px: { xs: 2, sm: 3, md: 4 },
          "@media (min-width: 1200px)": {
            px: 6,
          },
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 2,
          }}
        >
          <Typography
            variant="h4"
            component="h1"
            sx={{
              background: "linear-gradient(45deg, #2e7d32, #7b1fa2)",
              backgroundClip: "text",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            SAP CV-Analyse für Energiewirtschaft
          </Typography>
          <IconButton onClick={toggleColorMode} color="inherit" sx={{ ml: 2 }}>
            {mode === "dark" ? <LightMode /> : <DarkMode />}
          </IconButton>
        </Box>

        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 4,
                height: "100%",
                background: (theme) =>
                  theme.palette.mode === "light"
                    ? "linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.95))"
                    : "linear-gradient(135deg, rgba(26,28,30,0.9), rgba(26,28,30,0.95))",
                backdropFilter: "blur(20px)",
                border: (theme) =>
                  `1px solid ${
                    theme.palette.mode === "light"
                      ? "rgba(30, 132, 73, 0.1)"
                      : "rgba(39, 174, 96, 0.1)"
                  }`,
                borderRadius: 3,
                transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                "&:hover": {
                  boxShadow: (theme) =>
                    `0 16px 48px ${
                      theme.palette.mode === "light"
                        ? "rgba(30, 132, 73, 0.12)"
                        : "rgba(39, 174, 96, 0.12)"
                    }`,
                },
              }}
            >
              <Stack spacing={2}>
                <Typography variant="h6" gutterBottom>
                  Position auswählen
                </Typography>
                <Button
                  variant={
                    selectedRole === "developer" ? "contained" : "outlined"
                  }
                  onClick={() =>
                    handleRoleChange({ target: { value: "developer" } })
                  }
                  fullWidth
                  size="large"
                >
                  SAP Entwickler
                </Button>
                <Button
                  variant={
                    selectedRole === "consultant" ? "contained" : "outlined"
                  }
                  onClick={() =>
                    handleRoleChange({ target: { value: "consultant" } })
                  }
                  fullWidth
                  size="large"
                >
                  SAP Consultant
                </Button>

                <Box sx={{ mt: 4 }}>
                  <input
                    accept="application/pdf"
                    style={{ display: "none" }}
                    id="cv-file-upload"
                    type="file"
                    onChange={handleFileChange}
                  />
                  <label htmlFor="cv-file-upload">
                    <Button
                      variant="contained"
                      component="span"
                      startIcon={<UploadFile />}
                      fullWidth
                      size="large"
                    >
                      PDF-Lebenslauf hochladen
                    </Button>
                  </label>
                  {selectedFile && (
                    <Typography
                      variant="body2"
                      sx={{ mt: 1, color: "primary.main" }}
                    >
                      Ausgewählte Datei: {selectedFile.name}
                    </Typography>
                  )}
                </Box>
              </Stack>
            </Paper>
          </Grid>

          <Grid item xs={12} md={8}>
            <Paper
              elevation={0}
              sx={{
                p: 4,
                height: "100%",
                background: (theme) =>
                  theme.palette.mode === "light"
                    ? "linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.95))"
                    : "linear-gradient(135deg, rgba(26,28,30,0.9), rgba(26,28,30,0.95))",
                backdropFilter: "blur(20px)",
                border: (theme) =>
                  `1px solid ${
                    theme.palette.mode === "light"
                      ? "rgba(30, 132, 73, 0.1)"
                      : "rgba(39, 174, 96, 0.1)"
                  }`,
                borderRadius: 3,
                transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                "&:hover": {
                  boxShadow: (theme) =>
                    `0 16px 48px ${
                      theme.palette.mode === "light"
                        ? "rgba(30, 132, 73, 0.12)"
                        : "rgba(39, 174, 96, 0.12)"
                    }`,
                },
              }}
            >
              <Typography variant="h6" gutterBottom>
                Stellenanforderungen für{" "}
                {selectedRole === "developer"
                  ? "SAP Entwickler"
                  : "SAP Consultant"}
              </Typography>

              <TextField
                fullWidth
                multiline
                rows={15}
                value={requirements}
                onChange={handleRequirementsChange}
                variant="outlined"
                sx={{
                  mb: 3,
                  "& .MuiOutlinedInput-root": {
                    backgroundColor: (theme) =>
                      theme.palette.mode === "light"
                        ? "rgba(30, 132, 73, 0.02)"
                        : "rgba(39, 174, 96, 0.02)",
                    backdropFilter: "blur(20px)",
                    borderRadius: 3,
                    transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                    "&:hover": {
                      backgroundColor: (theme) =>
                        theme.palette.mode === "light"
                          ? "rgba(30, 132, 73, 0.05)"
                          : "rgba(39, 174, 96, 0.05)",
                      boxShadow: "0 8px 32px rgba(30, 132, 73, 0.1)",
                    },
                    "&.Mui-focused": {
                      backgroundColor: (theme) =>
                        theme.palette.mode === "light"
                          ? "rgba(30, 132, 73, 0.08)"
                          : "rgba(39, 174, 96, 0.08)",
                      boxShadow: "0 16px 48px rgba(30, 132, 73, 0.15)",
                    },
                  },
                }}
              />

              {error && (
                <Alert
                  severity="error"
                  sx={{
                    mt: 2,
                    borderRadius: 2,
                  }}
                >
                  {error}
                </Alert>
              )}

              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={loading}
                size="large"
                sx={{
                  mt: 2,
                  py: 1.5,
                  width: "100%",
                }}
              >
                {loading ? <CircularProgress size={24} /> : "Analyse starten"}
              </Button>
            </Paper>
          </Grid>
        </Grid>

        {results && (
          <Paper
            elevation={0}
            sx={{
              mt: 3,
              p: 3,
              border: (theme) =>
                `1px solid ${
                  theme.palette.mode === "light"
                    ? "rgba(46, 125, 50, 0.2)"
                    : "rgba(46, 125, 50, 0.1)"
                }`,
              borderRadius: 2,
            }}
          >
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                background: (theme) =>
                  `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                backgroundClip: "text",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                textShadow: (theme) =>
                  `0 0 20px ${alpha(theme.palette.primary.main, 0.3)}`,
              }}
            >
              Analyseergebnisse
            </Typography>

            {results.summary && results.summary.startsWith("Fehler") ? (
              <Alert
                severity="error"
                sx={{
                  mb: 2,
                  backgroundColor: (theme) =>
                    theme.palette.mode === "dark"
                      ? alpha(theme.palette.error.main, 0.1)
                      : alpha(theme.palette.error.light, 0.1),
                  color: "error.main",
                  border: 1,
                  borderColor: "error.main",
                }}
              >
                {results.summary}
              </Alert>
            ) : (
              <>
                <Paper
                  elevation={1}
                  sx={{
                    p: 3,
                    mb: 3,
                    background: "none",
                    border: (theme) =>
                      `1px solid ${
                        theme.palette.mode === "dark"
                          ? "rgba(255,255,255,0.1)"
                          : "rgba(0,0,0,0.1)"
                      }`,
                    transition: "all 0.3s ease-in-out",
                    "&:hover": {
                      boxShadow: (theme) =>
                        `0 16px 48px ${
                          theme.palette.mode === "light"
                            ? "rgba(30, 132, 73, 0.12)"
                            : "rgba(39, 174, 96, 0.12)"
                        }`,
                    },
                  }}
                >
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Box
                        sx={{ display: "flex", alignItems: "center", mb: 3 }}
                      >
                        <Box
                          sx={{
                            position: "relative",
                            display: "inline-flex",
                            mr: 3,
                            background: "transparent",
                            "&::after": {
                              content: '""',
                              position: "absolute",
                              top: -4,
                              left: -4,
                              right: -4,
                              bottom: -4,
                              borderRadius: "50%",
                              background: (theme) =>
                                `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                              opacity: 0.2,
                              animation: "pulse 2s ease-in-out infinite",
                            },
                          }}
                        >
                          <CircularProgress
                            variant="determinate"
                            value={results.overall_score}
                            size={80}
                            thickness={4}
                            sx={{
                              color: (theme) =>
                                results.overall_score > 70
                                  ? theme.palette.success.main
                                  : results.overall_score > 40
                                    ? theme.palette.warning.main
                                    : theme.palette.error.main,
                              boxShadow: (theme) =>
                                `0 0 20px ${alpha(
                                  results.overall_score > 70
                                    ? theme.palette.success.main
                                    : results.overall_score > 40
                                      ? theme.palette.warning.main
                                      : theme.palette.error.main,
                                  0.3,
                                )}`,
                            }}
                          />
                          <Box
                            sx={{
                              top: 0,
                              left: 0,
                              bottom: 0,
                              right: 0,
                              position: "absolute",
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "center",
                            }}
                          >
                            <Typography
                              variant="h6"
                              component="div"
                              sx={{
                                color: (theme) =>
                                  results.overall_score > 70
                                    ? theme.palette.mode === "light"
                                      ? "#1b5e20"
                                      : "#81c784"
                                    : results.overall_score > 40
                                      ? theme.palette.mode === "light"
                                        ? "#e65100"
                                        : "#ffb74d"
                                      : theme.palette.mode === "light"
                                        ? "#c62828"
                                        : "#ef9a9a",
                                fontWeight: "bold",
                              }}
                            >
                              {`${Math.round(results.overall_score)}%`}
                            </Typography>
                          </Box>
                        </Box>
                        <Box>
                          <Typography
                            variant="h5"
                            sx={{ color: "primary.main", mb: 0.5 }}
                          >
                            Gesamtbewertung
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Übereinstimmung mit dem Anforderungsprofil
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Box
                        sx={{ display: "flex", alignItems: "center", mb: 3 }}
                      >
                        <Box
                          sx={{
                            position: "relative",
                            display: "inline-flex",
                            mr: 3,
                            background: "transparent",
                          }}
                        >
                          <Chip
                            label={results.seniority_level}
                            color="primary"
                            sx={{
                              fontSize: "1.2rem",
                              fontWeight: "bold",
                              py: 2.5,
                              px: 3,
                              borderRadius: 2,
                              background: (theme) =>
                                `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                              color: "#ffffff",
                              boxShadow: (theme) =>
                                `0 4px 20px ${alpha(theme.palette.primary.main, 0.4)}`,
                            }}
                          />
                        </Box>
                        <Box>
                          <Typography
                            variant="h5"
                            sx={{ color: "primary.main", mb: 0.5 }}
                          >
                            Erfahrungsstufe
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Basierend auf den Qualifikationen
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>

                  <Typography
                    variant="body1"
                    paragraph
                    sx={{
                      whiteSpace: "pre-line",
                      backgroundColor: (theme) =>
                        alpha(
                          theme.palette.background.paper,
                          theme.palette.mode === "dark" ? 0.1 : 0.7,
                        ),
                      p: 2,
                      borderRadius: 1,
                      border: 1,
                      borderColor: "divider",
                      boxShadow: (theme) =>
                        `0 0 20px ${alpha(theme.palette.primary.main, 0.1)}`,
                    }}
                  >
                    {results.summary}
                  </Typography>

                  {results.key_strengths &&
                    results.key_strengths.length > 0 && (
                      <Box sx={{ mt: 3 }}>
                        <Typography
                          variant="subtitle1"
                          gutterBottom
                          color="primary.main"
                        >
                          Besondere Stärken:
                        </Typography>
                        <Box
                          sx={{
                            display: "flex",
                            flexWrap: "wrap",
                            gap: 1,
                            mb: 2,
                          }}
                        >
                          {results.key_strengths.map((strength, index) => (
                            <Chip
                              key={index}
                              label={strength}
                              color="success"
                              variant="outlined"
                              sx={{
                                fontSize: "0.9rem",
                                py: 0.5,
                                background: "none",
                                border: (theme) =>
                                  `1px solid ${
                                    theme.palette.mode === "dark"
                                      ? "rgba(255,255,255,0.1)"
                                      : "rgba(0,0,0,0.1)"
                                  }`,
                              }}
                            />
                          ))}
                        </Box>
                      </Box>
                    )}

                  {results.improvement_areas &&
                    results.improvement_areas.length > 0 && (
                      <Box sx={{ mt: 3 }}>
                        <Typography
                          variant="subtitle1"
                          gutterBottom
                          color="secondary.main"
                        >
                          Entwicklungspotenzial:
                        </Typography>
                        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                          {results.improvement_areas.map((area, index) => (
                            <Chip
                              key={index}
                              label={area}
                              color="secondary"
                              variant="outlined"
                              sx={{
                                fontSize: "0.9rem",
                                py: 0.5,
                                background: "none",
                                border: (theme) =>
                                  `1px solid ${
                                    theme.palette.mode === "dark"
                                      ? "rgba(255,255,255,0.1)"
                                      : "rgba(0,0,0,0.1)"
                                  }`,
                              }}
                            />
                          ))}
                        </Box>
                      </Box>
                    )}
                </Paper>

                {results.requirement_matches &&
                  results.requirement_matches.length > 0 && (
                    <>
                      <Typography
                        variant="h6"
                        gutterBottom
                        color="primary.main"
                      >
                        Detaillierte Analyse der Anforderungen:
                      </Typography>
                      <List>
                        {results.requirement_matches.map((match, index) => (
                          <ListItem key={index} sx={{ px: 0, mb: 2 }}>
                            <Paper
                              elevation={1}
                              sx={{
                                p: 2,
                                width: "100%",
                                background: "none",
                                border: (theme) =>
                                  `1px solid ${
                                    theme.palette.mode === "dark"
                                      ? "rgba(255,255,255,0.1)"
                                      : "rgba(0,0,0,0.1)"
                                  }`,
                                transition:
                                  "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                                "&:hover": {
                                  boxShadow: (theme) =>
                                    `0 8px 24px ${
                                      theme.palette.mode === "light"
                                        ? "rgba(30, 132, 73, 0.12)"
                                        : "rgba(39, 174, 96, 0.12)"
                                    }`,
                                },
                              }}
                            >
                              <Box
                                sx={{
                                  display: "flex",
                                  alignItems: "center",
                                  mb: 1,
                                }}
                              >
                                <Typography
                                  variant="subtitle2"
                                  sx={{
                                    flex: 1,
                                    color: "text.primary",
                                    fontWeight: 500,
                                  }}
                                >
                                  {match.requirement}
                                </Typography>
                                <Chip
                                  label={`${match.match_percentage}%`}
                                  color={
                                    match.match_percentage > 70
                                      ? "success"
                                      : match.match_percentage > 40
                                        ? "warning"
                                        : "error"
                                  }
                                  sx={{
                                    ml: 2,
                                    fontWeight: "bold",
                                    color: (theme) =>
                                      theme.palette.mode === "dark"
                                        ? "#ffffff"
                                        : "#000000",
                                    backgroundColor: (theme) => {
                                      const isLight =
                                        theme.palette.mode === "light";
                                      if (match.match_percentage > 70) {
                                        return isLight
                                          ? alpha("#2e7d32", 0.15)
                                          : alpha("#2e7d32", 0.35);
                                      } else if (match.match_percentage > 40) {
                                        return isLight
                                          ? alpha("#ed6c02", 0.15)
                                          : alpha("#ed6c02", 0.35);
                                      } else {
                                        return isLight
                                          ? alpha("#d32f2f", 0.15)
                                          : alpha("#d32f2f", 0.35);
                                      }
                                    },
                                    "& .MuiChip-label": {
                                      color: (theme) => {
                                        const isLight =
                                          theme.palette.mode === "light";
                                        if (match.match_percentage > 70) {
                                          return isLight
                                            ? "#1b5e20"
                                            : "#81c784";
                                        } else if (
                                          match.match_percentage > 40
                                        ) {
                                          return isLight
                                            ? "#e65100"
                                            : "#ffb74d";
                                        } else {
                                          return isLight
                                            ? "#c62828"
                                            : "#ef9a9a";
                                        }
                                      },
                                    },
                                  }}
                                />
                              </Box>
                              <Typography
                                variant="body2"
                                sx={{
                                  color: "text.secondary",
                                  whiteSpace: "pre-line",
                                  p: 1.5,
                                  borderRadius: 1,
                                  border: "1px solid",
                                  borderColor: "divider",
                                }}
                              >
                                {match.explanation}
                              </Typography>
                            </Paper>
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}

                {results.cv_text && (
                  <Box sx={{ mt: 4 }}>
                    <Typography
                      variant="subtitle1"
                      gutterBottom
                      color="text.secondary"
                    >
                      Extrahierter Text (Ausschnitt):
                    </Typography>
                    <Paper
                      elevation={1}
                      sx={{
                        p: 2,
                        background: "none",
                        border: (theme) =>
                          `1px solid ${
                            theme.palette.mode === "dark"
                              ? "rgba(255,255,255,0.1)"
                              : "rgba(0,0,0,0.1)"
                          }`,
                      }}
                    >
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                          whiteSpace: "pre-line",
                          fontFamily: "monospace",
                        }}
                      >
                        {results.cv_text}
                      </Typography>
                    </Paper>
                  </Box>
                )}
              </>
            )}
          </Paper>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
