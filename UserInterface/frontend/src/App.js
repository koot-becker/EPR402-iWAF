import React, { Component } from "react";
import WafItem from "./components/WafItem";
import Modal from "./components/Modal";
import axios from "axios";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wafs: [],
      modal: false,
      activeItem: {
        id: "",
        name: "",
        description: "",
        waf_details_path: "",
        start_waf_path: "",
        waf_address: "",
        start_web_app_path: "",
        web_app_address: "",
        total_requests: 0,
        allowed_requests: 0,
        blocked_requests: 0,
        threats_detected: 0,
        enabled: false,
      },
    };
  }

  componentDidMount() {
    this.refreshList();
    document.title = 'WAF Overview';
  }

  refreshList = () => {
    axios
      .get("/api/wafs/")
      .then((res) => this.setState({ wafs: res.data }))
      .catch((err) => console.log(err));
  };

  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };

  handleSubmit = (item) => {
    this.toggle();

    if (item.id) {
      axios
        .put(`/api/wafs/${item.id}/`, item)
        .then((res) => this.refreshList());
      return;
    }
    axios
      .post("/api/wafs/", item)
      .then((res) => this.refreshList());
  };

  handleDelete = (item) => {
    axios
      .delete(`/api/wafs/${item.id}/`)
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = {
      id: "",
      name: "",
      description: "",
      waf_details_path: "",
      start_waf_path: "",
      waf_address: "",
      start_web_app_path: "",
      web_app_address: "",
      total_requests: 0,
      allowed_requests: 0,
      blocked_requests: 0,
      threats_detected: 0,
      enabled: false,
    };

    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  renderItems = () => {
    return this.state.wafs.map((item) => (
      <WafItem
        key={item.id}
        item={item}
        editItem={this.editItem}
        handleDelete={this.handleDelete}
      />
    ));
  };

  render() {
    const { wafs, modal, activeItem } = this.state;

    return (
      <div className="container">
      <header>
        <h1>Web Application Firewall Overview</h1>
      </header>
      <main>
        <div className="row">
        {wafs.map((app, index) => (
          <div className="col-md-4" key={index}>
          <div className="card">
            <div className="card-body">
            <h2 className="card-title">{app.name}</h2>
            <p className="card-text">Description: {app.description}</p>
            <p className="card-text">WAF Address: {app.waf_address}</p>
            <p className="card-text">Web App Address: {app.web_app_address}</p>
            <p className="card-text">Total Requests: {app.total_requests}</p>
            <p className="card-text">Allowed Requests: {app.allowed_requests}</p>
            <p className="card-text">Blocked Requests: {app.blocked_requests}</p>
            <p className="card-text">Threats Detected: {app.threats_detected}</p>
            <p className="card-text">Enabled: {app.enabled ? "Yes" : "No"}</p>
            <div className="button-container">
              <button
              className="btn btn-primary"
              onClick={() => this.editItem(app)}
              >
              View Details
              </button>
              <button
              className="btn btn-primary"
              >
              Start WAF
              </button>
              <button
              className="btn btn-primary"
              >
              Start Web App
              </button>
            </div>
            <div className="button-container">
              <button
              className="btn btn-primary"
              >
              View WAF
              </button>
              <button
              className="btn btn-primary"
              >
              View Web App
              </button>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart
              margin={{
                top: 20,
                right: 20,
                bottom: 20,
                left: 20,
              }}
              >
                <CartesianGrid />
                <XAxis type="number" dataKey="x" name="True Negative" unit="%" domain={[0, 100]} label={{ value: 'True Negative', angle: 0, position: 'insideBottom', offset: -10 }} />
                <YAxis type="number" dataKey="y" name="True Positive" unit="%" domain={[0, 100]} label={{ value: 'True Positive', angle: -90, position: 'insideLeft', offset: 0 }} />
                <ReferenceLine  y={90} stroke="red" strokeDasharray="4 4" />
                <ReferenceLine x={90} stroke="red" strokeDasharray="4 4" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter 
                  name="Efficacy"
                  data={[{
                  x: app.blocked_requests, 
                  y: app.allowed_requests
                  }]} 
                  fill="#8884d8" 
                />
              </ScatterChart>
            </ResponsiveContainer>
            </div>
          </div>
          </div>
        ))}
        </div>
      </main>
      <footer>
        <p>WebAppFirewall 2024</p>
      </footer>
      {modal ? (
        <Modal
        activeItem={activeItem}
        toggle={this.toggle}
        onSave={this.handleSubmit}
        />
      ) : null}
      </div>
    );
  }
}

export default App;
