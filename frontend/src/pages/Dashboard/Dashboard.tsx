import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  useTheme,
  Stack,
  CircularProgress,
  Alert,
  Divider,
  IconButton,
  Menu,
  MenuItem,
  Pagination,
} from '@mui/material';
import {
  TrendingUp,
  Assignment,
  CheckCircle,
  Error,
  Schedule,
  Security,
  Person,
  Login,
  Search,
  Download,
  GetApp,
  Refresh,
  FilterList,
  Edit as EditIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { auditService } from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [auditStats, setAuditStats] = useState<any>(null);
  const [recentLogs, setRecentLogs] = useState<any[]>([]);
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null);
  const [availableActions, setAvailableActions] = useState<string[]>([]);
  const [selectedAction, setSelectedAction] = useState<string>('');
  const [logsPage, setLogsPage] = useState(1);
  const [logsPerPage] = useState(10);
  const [totalLogs, setTotalLogs] = useState(0);
  const [loadingLogs, setLoadingLogs] = useState(false);

  // Referencias para controlar la carga única de datos
  const isStatisticsLoaded = useRef(false);
  const isActionsLoaded = useRef(false);
  const isInitialLoadComplete = useRef(false);
  
  // Función separada para cargar las acciones únicas
  const loadUniqueActions = useCallback(async () => {
    // Solo cargar las acciones si aún no se han cargado
    if (!isActionsLoaded.current && availableActions.length === 0) {
      try {
        // Cargamos una muestra grande para obtener acciones únicas
        const allLogsResponse = await auditService.getLogsLegacy({ skip: 0, limit: 100 });
        const allLogsData = allLogsResponse.items || [];
        
        // Extraer acciones únicas y filtrar las relacionadas con personas
        const actionsSet = new Set<string>();
        allLogsData.forEach((log: any) => {
          if (log.action && typeof log.action === 'string') {
            // Filtrar solo acciones relevantes para el core de personas
            if (log.action.includes('PERSON') || 
                log.action === 'CREATE' || 
                log.action === 'UPDATE' || 
                log.action === 'DELETE' || 
                log.action === 'SEARCH_PERSON_BY_RUT' ||
                log.action === 'LIST_PERSONS' ||
                log.resource === 'persons') {
              actionsSet.add(log.action);
            }
          }
        });
        
        const uniqueActions = Array.from(actionsSet);
        setAvailableActions(uniqueActions);
        isActionsLoaded.current = true;
      } catch (err: any) {
        console.error('Error al cargar acciones únicas:', err);
      }
    }
  }, [availableActions.length]);

  // Función principal para cargar datos del dashboard
  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      // Función para cargar solo las estadísticas
      const loadStatistics = async () => {
        // Evitar cargar las estadísticas si ya se cargaron previamente
        if (!isStatisticsLoaded.current) {
          try {
            const stats = await auditService.getStats(30);
            setAuditStats(stats);
            isStatisticsLoaded.current = true;
          } catch (err: any) {
            console.error('Error al cargar estadísticas:', err);
            throw err;
          }
        }
      };

      // Función para cargar logs, con opciones de paginación y filtrado
      const loadLogs = async (page: number = 1, action: string = '') => {
        try {
          setLoadingLogs(true);
          
          // Parámetros para la solicitud paginada
          const params: any = {
            skip: (page - 1) * logsPerPage,
            limit: logsPerPage,
          };
          
          // Aplicar filtro por acción si existe
          if (action) {
            params.action = action;
          }

          // Cargar logs paginados para la tabla
          const response = await auditService.getLogsLegacy(params);
          const logs = response.items || [];
          setRecentLogs(logs);
          setTotalLogs(response.total || 0);
          
          // Cargar acciones únicas solo una vez
          await loadUniqueActions();
          
        } catch (err: any) {
          console.error('Error al cargar logs:', err);
        } finally {
          setLoadingLogs(false);
        }
      };

      // Cargamos los datos en paralelo para mejorar el rendimiento
      await Promise.all([
        loadStatistics(),
        loadLogs(logsPage, selectedAction)
      ]);

    } catch (err: any) {
      console.error('Error al cargar los datos del dashboard:', err);
      setError(err.message || 'Error al cargar los datos del dashboard');
    } finally {
      setLoading(false);
    }
  }, [logsPage, logsPerPage, selectedAction, loadUniqueActions]);
  
  // Cargar datos al montar el componente
  useEffect(() => {
    if (!isInitialLoadComplete.current) {
      loadDashboardData();
      isInitialLoadComplete.current = true;
    }
  }, [loadDashboardData]);

  const handleExportLogs = async (format: 'csv' | 'json' = 'csv') => {
    try {
      setExporting(true);
      setExportMenuAnchor(null);
      const blob = await auditService.exportLogs({ format });
      
      // Crear un enlace de descarga
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `audit_logs_${new Date().toISOString().split('T')[0]}.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(`Error al exportar logs: ${err.message}`);
    } finally {
      setExporting(false);
    }
  };

  const handleOpenExportMenu = (event: React.MouseEvent<HTMLElement>) => {
    setExportMenuAnchor(event.currentTarget);
  };

  const handleCloseExportMenu = () => {
    setExportMenuAnchor(null);
  };

  // Manejador optimizado para el cambio de filtro por acción
  const handleActionFilterChange = (action: string) => {
    // Si se selecciona la misma acción, resetear el filtro
    const newAction = action === selectedAction ? '' : action;
    // Actualizar el estado del filtro
    setSelectedAction(newAction);
    // Resetear a la página 1 al cambiar de filtro
    setLogsPage(1);
    // Recargar dashboard con el nuevo filtro
    loadDashboardData();
  };

  // Manejador optimizado para la paginación
  const handleLogsPageChange = (event: React.ChangeEvent<unknown>, page: number) => {
    // Actualizar página actual
    setLogsPage(page);
    // Recargar dashboard con la nueva página
    loadDashboardData();
  };

  // Manejador para recargar datos, que respeta los filtros actuales
  const handleRefreshData = () => {
    // Solo recargamos estadísticas si el botón de recarga se presiona explícitamente
    isStatisticsLoaded.current = false;
    // Cargar todos los datos nuevamente
    loadDashboardData();
  };

  if (loading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '60vh',
        gap: 2
      }}>
        <CircularProgress size={48} thickness={4} />
        <Typography variant="body1" color="text.secondary">
          Cargando datos del dashboard...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={handleRefreshData}>
            Reintentar
          </Button>
        }>
          {error}
        </Alert>
      </Box>
    );
  }

  // Estas funciones están comentadas porque actualmente no se usan, pero pueden ser útiles en el futuro
  
  /* Función auxiliar para sumar valores de acciones que pueden tener distintos nombres
  const sumActionValues = (actionKeys: string[]) => {
    if (!auditStats?.actions_by_type) return 0;
    return actionKeys.reduce((sum, key) => {
      return sum + (auditStats.actions_by_type[key] || 0);
    }, 0);
  };
  */

  /* Verificar si los recursos son del tipo "persons"
  const getPersonsResourceCount = (resourceType: string) => {
    if (!auditStats?.resources_by_type) return 0;
    return auditStats.resources_by_type[resourceType] || 0;
  };
  */

  // Según la respuesta real de la API, ajustamos los contadores
  const stats = [
    { 
      title: 'Personas Registradas', 
      value: auditStats?.actions_by_type?.CREATE || 0, 
      icon: <Person />, 
      color: theme.palette.primary.main 
    },
    { 
      title: 'Modificaciones', 
      value: auditStats?.actions_by_type?.UPDATE || 0, 
      icon: <EditIcon />, 
      color: theme.palette.info.main 
    },
    { 
      title: 'Búsquedas por RUT', 
      value: (auditStats?.actions_by_type?.SEARCH_SUCCESS || 0) + (auditStats?.actions_by_type?.SEARCH_FAILED || 0), 
      icon: <Search />, 
      color: theme.palette.warning.main 
    },
    { 
      title: 'Consultas Generales', 
      value: auditStats?.actions_by_type?.READ || 0,
      icon: <Assignment />, 
      color: theme.palette.success.main 
    },
  ];

  // Datos para gráficos basados en estadísticas reales
  const chartData = {
    labels: auditStats?.daily_actions?.map((day: any) => day.date) || [],
    datasets: [
      {
        label: 'Operaciones Diarias en Personas',
        data: auditStats?.daily_actions?.map((day: any) => day.count) || [],
        backgroundColor: theme.palette.primary.main,
        borderColor: theme.palette.primary.dark,
        borderWidth: 1,
      },
    ],
  };

  const hourlyData = {
    labels: auditStats?.hourly_distribution?.map((hour: any) => `${hour.hour}:00`) || [],
    datasets: [
      {
        label: 'Distribución por Hora',
        data: auditStats?.hourly_distribution?.map((hour: any) => hour.count) || [],
        backgroundColor: theme.palette.secondary.main,
        borderColor: theme.palette.secondary.dark,
        borderWidth: 1,
      },
    ],
  };

  const resourcesData = {
    labels: Object.keys(auditStats?.resources_by_type || {}),
    datasets: [
      {
        data: Object.values(auditStats?.resources_by_type || {}),
        backgroundColor: [
          theme.palette.primary.main,
          theme.palette.success.main,
          theme.palette.warning.main,
          theme.palette.error.main,
          theme.palette.info.main,
        ],
        borderWidth: 0,
      },
    ],
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'LOGIN_SUCCESS': return <Login />;
      case 'CREATE_PERSON': return <Person />;
      case 'UPDATE_PERSON': return <CheckCircle />;
      case 'DELETE_PERSON': return <Error />;
      case 'SEARCH': 
      case 'SEARCH_PERSON_BY_RUT': return <Search />;
      default: return <Assignment />;
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'LOGIN_SUCCESS': return theme.palette.success.main;
      case 'CREATE_PERSON': return theme.palette.primary.main;
      case 'UPDATE_PERSON': return theme.palette.info.main;
      case 'DELETE_PERSON': return theme.palette.error.main;
      case 'SEARCH': 
      case 'SEARCH_PERSON_BY_RUT': return theme.palette.warning.main;
      default: return theme.palette.grey[500];
    }
  };

  const formatActionLabel = (action: string) => {
    const labels: { [key: string]: string } = {
      'LOGIN_SUCCESS': 'Inicio de Sesión',
      'CREATE_PERSON': 'Persona Registrada',
      'UPDATE_PERSON': 'Persona Modificada',
      'DELETE_PERSON': 'Persona Eliminada',
      'SEARCH': 'Búsqueda General',
      'SEARCH_PERSON_BY_RUT': 'Búsqueda por RUT',
      'LIST_PERSONS': 'Consulta de Listado',
      'READ': 'Consulta de Datos',
    };
    return labels[action] || action;
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* Header */}
      <Box sx={{ 
        mb: 4, 
        p: 3, 
        borderRadius: 3, 
        background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
        color: 'white',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <Box sx={{ position: 'relative', zIndex: 2 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h3" component="h1" sx={{ fontWeight: 700, mb: 1 }}>
                Dashboard Core Personas
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                Monitoreo y auditoría del sistema de gestión de personas
              </Typography>
            </Box>
            <Stack direction="row" spacing={1}>
              <IconButton
                color="inherit"
                onClick={handleOpenExportMenu}
                disabled={loading || exporting}
                sx={{ bgcolor: 'rgba(255,255,255,0.1)', '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' } }}
              >
                <GetApp />
              </IconButton>
              <IconButton
                color="inherit"
                onClick={handleRefreshData}
                disabled={loading}
                sx={{ bgcolor: 'rgba(255,255,255,0.1)', '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' } }}
              >
                <Refresh />
              </IconButton>
            </Stack>
          </Stack>
        </Box>
        <Box sx={{ 
          position: 'absolute', 
          top: 0, 
          right: 0, 
          width: '200px', 
          height: '200px', 
          background: 'rgba(255,255,255,0.1)', 
          borderRadius: '50%',
          transform: 'translate(50%, -50%)',
        }} />
      </Box>

      {/* Export Menu */}
      <Menu
        anchorEl={exportMenuAnchor}
        open={Boolean(exportMenuAnchor)}
        onClose={handleCloseExportMenu}
      >
        <MenuItem onClick={() => handleExportLogs('csv')} disabled={exporting}>
          <Download sx={{ mr: 1 }} />
          Exportar CSV
        </MenuItem>
        <MenuItem onClick={() => handleExportLogs('json')} disabled={exporting}>
          <Download sx={{ mr: 1 }} />
          Exportar JSON
        </MenuItem>
      </Menu>

      {/* Stats Cards */}
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr 1fr' }, 
        gap: 3, 
        mb: 4 
      }}>
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card sx={{ 
              height: '100%', 
              background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
              border: `1px solid ${stat.color}40`,
              position: 'relative',
              overflow: 'hidden',
            }}>
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h3" component="div" sx={{ 
                      fontWeight: 700, 
                      color: stat.color,
                      mb: 1,
                    }}>
                      {stat.value.toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 500 }}>
                      {stat.title}
                    </Typography>
                  </Box>
                  <Box sx={{ 
                    position: 'relative',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      background: `linear-gradient(135deg, ${stat.color}20, transparent)`,
                      borderRadius: '50%',
                      transform: 'scale(1.2)',
                    }
                  }}>
                    <Avatar sx={{ 
                      bgcolor: stat.color, 
                      width: 56, 
                      height: 56,
                      position: 'relative',
                      zIndex: 1,
                    }}>
                      {stat.icon}
                    </Avatar>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </Box>

      {/* Charts */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '2fr 1fr' }, gap: 3, mb: 4 }}>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card sx={{ 
            background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
            border: '1px solid #475569',
          }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ mr: 1, color: theme.palette.primary.main }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Actividad Diaria - Core Personas
                </Typography>
              </Box>
              <Box sx={{ height: 300 }}>
                <Bar 
                  data={chartData} 
                  options={{ 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        labels: {
                          color: '#cbd5e1'
                        }
                      }
                    },
                    scales: {
                      x: {
                        ticks: {
                          color: '#94a3b8'
                        },
                        grid: {
                          color: '#334155'
                        }
                      },
                      y: {
                        ticks: {
                          color: '#94a3b8'
                        },
                        grid: {
                          color: '#334155'
                        }
                      }
                    }
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card sx={{ 
            background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
            border: '1px solid #475569',
          }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Assignment sx={{ mr: 1, color: theme.palette.secondary.main }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Operaciones por Recurso
                </Typography>
              </Box>
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Doughnut 
                  data={resourcesData} 
                  options={{ 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        labels: {
                          color: '#cbd5e1'
                        }
                      }
                    }
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Box>

      {/* Second row of charts */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3, mb: 4 }}>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card sx={{ 
            background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
            border: '1px solid #475569',
          }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Schedule sx={{ mr: 1, color: theme.palette.warning.main }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Distribución por Horas
                </Typography>
              </Box>
              <Box sx={{ height: 250 }}>
                <Bar 
                  data={hourlyData} 
                  options={{ 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        labels: {
                          color: '#cbd5e1'
                        }
                      }
                    },
                    scales: {
                      x: {
                        ticks: {
                          color: '#94a3b8'
                        },
                        grid: {
                          color: '#334155'
                        }
                      },
                      y: {
                        ticks: {
                          color: '#94a3b8'
                        },
                        grid: {
                          color: '#334155'
                        }
                      }
                    }
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card sx={{ 
            background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
            border: '1px solid #475569',
          }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Person sx={{ mr: 1, color: theme.palette.success.main }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Usuarios Activos del Sistema
                </Typography>
              </Box>
              <List>
                {auditStats?.most_active_users?.slice(0, 3).map((user: any, index: number) => (
                  <ListItem key={user.user_id} sx={{ 
                    borderRadius: 2, 
                    mb: 1,
                    bgcolor: 'rgba(255,255,255,0.03)',
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.08)'
                    }
                  }}>
                    <ListItemAvatar>
                      <Avatar sx={{ 
                        bgcolor: theme.palette.primary.main,
                        background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`
                      }}>
                        <Person />
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {user.user_email}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="body2" color="text.secondary">
                          {user.actions_count} acciones
                        </Typography>
                      }
                    />
                    <Chip 
                      label={`#${index + 1}`}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </ListItem>
                )) || (
                  <ListItem>
                    <ListItemText 
                      primary={
                        <Typography color="text.secondary">
                          No hay datos de usuarios
                        </Typography>
                      } 
                    />
                  </ListItem>
                )}
              </List>
            </CardContent>
          </Card>
        </motion.div>
      </Box>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card sx={{ 
          background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
          border: '1px solid #475569',
        }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Security sx={{ mr: 1, color: theme.palette.info.main }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Actividad Reciente - Core Personas
                </Typography>
              </Box>
              
              <Chip 
                icon={<FilterList />}
                label={`${totalLogs} registros`}
                size="small"
                variant="outlined"
                sx={{ 
                  borderColor: '#475569',
                  color: '#94a3b8'
                }}
              />
            </Box>

            {/* Filtros por acción usando chips */}
            {availableActions.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Filtrar por tipo de acción:
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                  <Chip
                    label="Todas"
                    onClick={() => handleActionFilterChange('')}
                    variant={selectedAction === '' ? 'filled' : 'outlined'}
                    color={selectedAction === '' ? 'primary' : 'default'}
                    size="small"
                    sx={{ 
                      mb: 1,
                      borderColor: selectedAction === '' ? theme.palette.primary.main : '#475569',
                      color: selectedAction === '' ? 'white' : '#94a3b8',
                      '&:hover': {
                        bgcolor: selectedAction === '' ? theme.palette.primary.dark : 'rgba(255,255,255,0.05)',
                      }
                    }}
                  />
                  {availableActions.map((action) => (
                    <Chip
                      key={action}
                      label={formatActionLabel(action)}
                      onClick={() => handleActionFilterChange(action)}
                      variant={selectedAction === action ? 'filled' : 'outlined'}
                      color={selectedAction === action ? 'primary' : 'default'}
                      size="small"
                      icon={getActionIcon(action)}
                      sx={{ 
                        mb: 1,
                        borderColor: selectedAction === action ? getActionColor(action) : '#475569',
                        color: selectedAction === action ? 'white' : '#94a3b8',
                        bgcolor: selectedAction === action ? getActionColor(action) : 'transparent',
                        '&:hover': {
                          bgcolor: selectedAction === action ? getActionColor(action) + 'CC' : getActionColor(action) + '20',
                          borderColor: getActionColor(action),
                          color: selectedAction === action ? 'white' : getActionColor(action),
                        }
                      }}
                    />
                  ))}
                </Stack>
              </Box>
            )}
            
            {loadingLogs ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                <CircularProgress size={24} />
              </Box>
            ) : (
              <List>
              {recentLogs.length === 0 ? (
                <ListItem sx={{ 
                  textAlign: 'center', 
                  py: 4,
                  bgcolor: 'rgba(255,255,255,0.02)',
                  borderRadius: 2,
                }}>
                  <ListItemText 
                    primary={
                      <Typography variant="body1" color="text.secondary">
                        No hay actividad reciente
                      </Typography>
                    }
                    secondary={
                      <Typography variant="body2" color="text.secondary">
                        No se encontraron registros de auditoría
                      </Typography>
                    }
                  />
                </ListItem>
              ) : (
                recentLogs.map((log: any, index: number) => (
                  <ListItem 
                    key={log.id} 
                    divider={index < recentLogs.length - 1}
                    sx={{ 
                      borderRadius: 2, 
                      mb: 1,
                      bgcolor: 'rgba(255,255,255,0.02)',
                      '&:hover': {
                        bgcolor: 'rgba(255,255,255,0.05)'
                      }
                    }}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ 
                        bgcolor: getActionColor(log.action),
                        background: `linear-gradient(135deg, ${getActionColor(log.action)}, ${getActionColor(log.action)}CC)`
                      }}>
                        {getActionIcon(log.action)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                          {log.details}
                        </Typography>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          <Stack direction="row" spacing={1} sx={{ mb: 1, flexWrap: 'wrap' }}>
                            <Chip 
                              label={formatActionLabel(log.action)} 
                              size="small" 
                              sx={{ 
                                backgroundColor: getActionColor(log.action) + '30',
                                color: getActionColor(log.action),
                                fontWeight: 600,
                                border: `1px solid ${getActionColor(log.action)}50`
                              }} 
                            />
                            <Chip 
                              label={log.resource} 
                              size="small" 
                              variant="outlined"
                              sx={{ 
                                borderColor: '#475569',
                                color: '#94a3b8'
                              }}
                            />
                          </Stack>
                          <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Person sx={{ fontSize: 14 }} />
                            {log.user_email} • {new Date(log.timestamp).toLocaleString('es-ES')}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))
              )}
            </List>
            )}
            
            {/* Paginación */}
            {totalLogs > logsPerPage && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <Pagination
                  count={Math.ceil(totalLogs / logsPerPage)}
                  page={logsPage}
                  onChange={handleLogsPageChange}
                  color="primary"
                  sx={{
                    '& .MuiPaginationItem-root': {
                      color: '#94a3b8',
                      '&:hover': {
                        bgcolor: 'rgba(59, 130, 246, 0.1)',
                      },
                      '&.Mui-selected': {
                        bgcolor: theme.palette.primary.main,
                        color: 'white',
                        '&:hover': {
                          bgcolor: theme.palette.primary.dark,
                        },
                      },
                    },
                  }}
                />
              </Box>
            )}
          </CardContent>
          <Divider sx={{ borderColor: '#475569' }} />
          <CardActions sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.02)' }}>
            <Button 
              size="small" 
              startIcon={<Security />}
              variant="outlined"
              sx={{ 
                borderColor: theme.palette.info.main,
                color: theme.palette.info.main,
                '&:hover': {
                  bgcolor: theme.palette.info.main + '20'
                }
              }}
            >
              Ver Todos los Logs
            </Button>
            <Button 
              size="small" 
              startIcon={<Download />}
              onClick={() => handleExportLogs('csv')}
              disabled={exporting}
              variant="contained"
              sx={{ 
                ml: 1,
                background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`
              }}
            >
              {exporting ? 'Exportando...' : 'Exportar Logs'}
            </Button>
          </CardActions>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Dashboard;
