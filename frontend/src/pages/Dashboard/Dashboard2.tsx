import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  useTheme,
  Stack,
} from '@mui/material';
import {
  TrendingUp,
  Assignment,
  CheckCircle,
  Warning,
  Error,
  Schedule,
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

  const stats = [
    { title: 'Proyectos Activos', value: 12, icon: <Assignment />, color: theme.palette.primary.main },
    { title: 'Auditorías Completadas', value: 45, icon: <CheckCircle />, color: theme.palette.success.main },
    { title: 'Problemas Detectados', value: 23, icon: <Warning />, color: theme.palette.warning.main },
    { title: 'Críticos Pendientes', value: 5, icon: <Error />, color: theme.palette.error.main },
  ];

  const recentProjects = [
    { name: 'Sistema de Gestión CRM', status: 'En Progreso', progress: 75, priority: 'Alta' },
    { name: 'Aplicación Mobile Banking', status: 'Revisión', progress: 90, priority: 'Crítica' },
    { name: 'Portal de E-commerce', status: 'Iniciando', progress: 25, priority: 'Media' },
    { name: 'API de Integración', status: 'Completado', progress: 100, priority: 'Baja' },
  ];

  const chartData = {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Auditorías Completadas',
        data: [12, 19, 15, 25, 22, 30],
        backgroundColor: theme.palette.primary.main,
        borderColor: theme.palette.primary.dark,
        borderWidth: 1,
      },
    ],
  };

  const doughnutData = {
    labels: ['Completadas', 'En Progreso', 'Pendientes'],
    datasets: [
      {
        data: [45, 12, 8],
        backgroundColor: [
          theme.palette.success.main,
          theme.palette.warning.main,
          theme.palette.error.main,
        ],
        borderWidth: 0,
      },
    ],
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Crítica': return theme.palette.error.main;
      case 'Alta': return theme.palette.warning.main;
      case 'Media': return theme.palette.info.main;
      case 'Baja': return theme.palette.success.main;
      default: return theme.palette.grey[500];
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completado': return theme.palette.success.main;
      case 'En Progreso': return theme.palette.info.main;
      case 'Revisión': return theme.palette.warning.main;
      case 'Iniciando': return theme.palette.primary.main;
      default: return theme.palette.grey[500];
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        Dashboard de Auditoría
      </Typography>

      {/* Stats Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr 1fr' }, gap: 3, mb: 4 }}>
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card sx={{ 
              height: '100%', 
              background: `linear-gradient(135deg, ${stat.color}15 0%, ${stat.color}05 100%)`,
              border: `1px solid ${stat.color}30`,
            }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h3" component="div" sx={{ fontWeight: 'bold', color: stat.color }}>
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {stat.title}
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: stat.color, width: 56, height: 56 }}>
                    {stat.icon}
                  </Avatar>
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
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Progreso Mensual de Auditorías
              </Typography>
              <Box sx={{ height: 300 }}>
                <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
              </Box>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Estado de Proyectos
              </Typography>
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Doughnut data={doughnutData} options={{ responsive: true, maintainAspectRatio: false }} />
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Box>

      {/* Recent Projects */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Proyectos Recientes
            </Typography>
            <List>
              {recentProjects.map((project, index) => (
                <ListItem key={index} divider={index < recentProjects.length - 1}>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: getStatusColor(project.status) }}>
                      <Schedule />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={project.name}
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                          <Chip 
                            label={project.status} 
                            size="small" 
                            sx={{ 
                              backgroundColor: getStatusColor(project.status) + '20',
                              color: getStatusColor(project.status),
                              fontWeight: 'bold'
                            }} 
                          />
                          <Chip 
                            label={`Prioridad: ${project.priority}`} 
                            size="small" 
                            sx={{ 
                              backgroundColor: getPriorityColor(project.priority) + '20',
                              color: getPriorityColor(project.priority),
                              fontWeight: 'bold'
                            }} 
                          />
                        </Stack>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body2" color="text.secondary">
                            Progreso: {project.progress}%
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={project.progress} 
                            sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                          />
                        </Box>
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
          <CardActions>
            <Button size="small" startIcon={<TrendingUp />}>
              Ver Todos los Proyectos
            </Button>
          </CardActions>
        </Card>
      </motion.div>
    </Box>
  );
};

export default Dashboard;
