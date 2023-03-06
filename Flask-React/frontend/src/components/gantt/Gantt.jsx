
import "./gantt.scss"
// import { GanttComponent, TaskFieldsModel, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-gantt';
import * as ReactDOM from 'react-dom';
import { GanttComponent, ColumnsDirective, ColumnDirective, TaskFieldsModel } from '@syncfusion/ej2-react-gantt';
import { projectData } from './data';
// import { Gantt, Task, EventOption, StylingOption, ViewMode, DisplayOption, columnWidth } from 'gantt-task-react';
// import "gantt-task-react/dist/index.css";


const Ganttt = () => {


    const taskValues: TaskFieldsModel = {
    id: "TaskID",
    name: "TaskName",
    startDate: "StartDate",
    endDate: "EndDate",
    duration: "Duration",
    progress: "Progress",
    child: "subtasks",
    dependency: "Predeceesor"
  }




  return (

      
      <GanttComponent dataSource={projectData}
            taskFields={taskValues} width='1150px' >
        <ColumnsDirective>
          <ColumnDirective field="TaskID" headerText="ID"></ColumnDirective>
          <ColumnDirective field="TaskName" headerText="Name"></ColumnDirective>
          <ColumnDirective field="StartDate" format="dd-MMM-yy"></ColumnDirective>
          <ColumnDirective field="Duration" headerText="Duration"></ColumnDirective>
          </ColumnsDirective>
        </GanttComponent>
      
  )
}

export default Ganttt