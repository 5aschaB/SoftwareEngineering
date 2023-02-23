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
      project: "Project 1",
      deadline: "5 April",
      employee: "John Smith",
      status: "Approved",
    },
      {
      project: "Project 2",
      deadline: "12 March",
      employee: "John Smith",
      status: "Pending",
    },
    {
      project: "Project 3",
      deadline: "1 March",
      employee: "John Smith",
      status: "Approved",
    }
  ];
  return (
    <TableContainer component={Paper} className="table">
      <Table sx={{ minWidth: 650 }} className="tab" aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className="tableCell"> Project</TableCell>
            <TableCell className="tableCell">Deadline</TableCell>
            <TableCell className="tableCell">Employee</TableCell>
            <TableCell className="tableCell">Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.project}>
              <TableCell className="tableCell">{row.project}</TableCell>
              <TableCell className="tableCell">{row.deadline}</TableCell>
              <TableCell className="tableCell">{row.employee}</TableCell>
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