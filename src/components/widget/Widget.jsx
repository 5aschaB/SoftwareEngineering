import "./widget.scss"
import BugReportOutlinedIcon from '@mui/icons-material/BugReportOutlined';



export const Widget = () => {
  return (
      <div className="widget">
          <div className="left">
              <span className="title">GIT COMMITS</span>
              <span className="counter">3</span>
          </div>
          <div className="right">
              <div className="percentage">
                  <BugReportOutlinedIcon/>
              </div>
              
          </div>
    </div>
  )
}
