Object.defineProperty(exports, "__esModule", { value: true });

exports.projectData = [
    {
        TaskID: 1,
        TaskName: 'Project Initiation',
        StartDate: new Date('04/02/2023'),
        EndDate: new Date('04/21/2023'),
        subtasks: [
            { TaskID: 2, TaskName: 'Finalise budget, timeline and scope', StartDate: new Date('04/03/2023'), Duration: 4, Progress: 75 },
            { TaskID: 3, TaskName: 'Finish Requirements Analysis', StartDate: new Date('04/4/2023'), Duration: 4, Progress: 50, Predeceesor:"2FS" },
            { TaskID: 4, TaskName: 'Finish Design Document', StartDate: new Date('04/6/2023'), Duration: 4, Progress: 50 },
            { TaskID: 4, TaskName: 'Stakeholder Approval', StartDate: new Date('04/8/2023'), Duration: 4, Progress: 50 },
        ]
    },
    {
        TaskID: 5,
        TaskName: 'Project Development and Deployment',
        StartDate: new Date('04/02/2023'),
        EndDate: new Date('04/21/2023'),
        subtasks: [
            { TaskID: 6, TaskName: 'Develop frontend ', StartDate: new Date('04/10/2023'), Duration: 3, Progress: 50 },
            { TaskID: 7, TaskName: 'Develop backend', StartDate: new Date('04/12/2023'), Duration: 3, Progress: 60 },
            { TaskID: 8, TaskName: 'Market Research', StartDate: new Date('04/15/2023'), Duration: 3, Progress: 30 }
        ]
    },
];