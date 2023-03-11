import "./table.scss";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const List = () => {
  const rows = [
    {
      project: "Risk Management Software",
      deadline: "5 April",
      risk: "1",
      status: "Approved",
    },
      {
      project: "To-do List Application",
      deadline: "12 March",
      risk: "5",
      status: "Pending",
    },
    {
      project: "BMI Calculator Project",
      deadline: "1 March",
      risk: "3",
      status: "Approved",
    },
       {
      project: "Food Review Website",
      deadline: "18 March",
      risk: "2",
      status: "Pending",
    },
          {
      project: "Social Media Project",
      deadline: "26 April",
      risk: "1",
      status: "Pending",
    }
  ];
  return (
    <TableContainer component={Paper} className="table">
      <Table sx={{ minWidth: 650 }} className="tab" aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className="tableCell"> Project</TableCell>
            <TableCell className="tableCell">Deadline</TableCell>
            <TableCell className="tableCell"> <b>Risk (1-5) *</b> </TableCell>
            <TableCell className="tableCell">Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.project}>
              <TableCell className="tableCell">{row.project}</TableCell>
              <TableCell className="tableCell">{row.deadline}</TableCell>
              <TableCell className="tableCell">{row.risk}</TableCell>
              <TableCell className="tableCell">
                <span className={`status ${row.status}`}>{row.status}</span>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

};

export default List;