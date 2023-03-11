
import { Featured } from '../../components/featured/Featured'
import { Featured2 } from '../../components/featured2/Featured2'
import Navbar from '../../components/navbar/Navbar'
import Sidebar from '../../components/sidebar/Sidebar'
import { Widget } from '../../components/widget/Widget'
import { Chart } from '../../components/chart/Chart'
import Table from "../../components/table/Table";
import "./home.scss"
import Gantt from "../../components/gantt/Gantt";
  

const Home = () => {

  return (



      <div className='home'>
          <Sidebar/>
      <div className="homeContainer">
        <Navbar />
        <div className="widgets">
          <Widget />
        </div>
        <div className="charts">
          <Featured />
          <Featured2 />
          {/* <Chart title="Project Progress" /> */}
            <div className="listTitle"></div>
          {/* <Table /> */}
        </div>
        <div className="listContainer">
           <Gantt > </Gantt>
        </div>
        </div>
      </div>
  )
}

export default Home



