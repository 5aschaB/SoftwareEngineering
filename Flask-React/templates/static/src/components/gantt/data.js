Object.defineProperty(exports, "__esModule", { value: true });

exports.projectData = [
    {
        TaskID: 1,
        TaskName: 'Project Initiation',
        StartDate: new Date('04/02/2023'),
        EndDate: new Date('04/21/2023'),
        subtasks: [
            { TaskID: 2, TaskName: 'Identify Site location', StartDate: new Date('04/06/2023'), Duration: 4, Progress: 75 },
            { TaskID: 3, TaskName: 'Perform Soil test', StartDate: new Date('04/10/2023'), Duration: 4, Progress: 50, Predeceesor:"2FS" },
            { TaskID: 4, TaskName: 'Soil test approval', StartDate: new Date('04/12/2023'), Duration: 4, Progress: 50 },
            { TaskID: 4, TaskName: 'Soil test approval', StartDate: new Date('04/20/2023'), Duration: 4, Progress: 50 },
        ]
    },
    {
        TaskID: 5,
        TaskName: 'Project Estimation',
        StartDate: new Date('04/02/2023'),
        EndDate: new Date('04/21/2023'),
        subtasks: [
            { TaskID: 6, TaskName: 'Develop floor plan for estimation', StartDate: new Date('04/03/2023'), Duration: 3, Progress: 50 },
            { TaskID: 7, TaskName: 'List materials', StartDate: new Date('04/04/2023'), Duration: 3, Progress: 60 },
            { TaskID: 8, TaskName: 'Estimation approval', StartDate: new Date('04/08/2023'), Duration: 3, Progress: 30 }
        ]
    },
];