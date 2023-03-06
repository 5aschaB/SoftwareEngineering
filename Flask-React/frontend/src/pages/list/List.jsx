import "./list.scss"
import Sidebar from "../../components/sidebar/Sidebar"
import Navbar from "../../components/navbar/Navbar"
import ChatBot from 'react-simple-chatbot';
import { Segment } from 'semantic-ui-react'
import { ThemeProvider } from 'styled-components';



const List = () => {

const theme = {
  background: '#f5f8fb',
  fontFamily: 'Helvetica Neue',
  headerBgColor: '#fc4a28',
  headerFontColor: '#fff',
  headerFontSize: '15px',
  botBubbleColor: '#EF6C00',
  botFontColor: '#fff',
  userBubbleColor: '#fff',
  userFontColor: '#4a4a4a',
};

    const steps = [
    {
      id: "Greet",
      message: "Hello, Welcome to our shop",
      trigger: "Done",
    },
    {
      id: "Done",
      message: "Please enter your name!",
      trigger: "waiting1",
    },
    {
      id: "waiting1",
      user: true,
      trigger: "Name",
    },
    {
      id: "Name",
      message: "Hi {previousValue}, Please select your issue",
      trigger: "issues",
    },
    {
      id: "issues",
      options: [
        {
          value: "React",
          label: "React",
          trigger: "React",
        },
        { value: "Angular", label: "Angular", trigger: "Angular" },

      ],

    },
    {
      id: "React",
      message:
        "Thanks for letting your React issue, Our team will resolve your issue ASAP",
      end: true,
    },
    {
      id: "Angular",
      message:
        "Thanks for letting your Angular issue, Our team will resolve your issue ASAP",
      end: true,
    },
  ]; 

  return (
    <div className="list">
      <Sidebar />

      
      <div className="listContainer">
        <Navbar />
        
       <div className="chatbot">
   <ThemeProvider theme={theme}>
        <ChatBot steps={steps}/>
       </ThemeProvider>
      </div>
    
      </div>
    </div>
  )
}

export default List