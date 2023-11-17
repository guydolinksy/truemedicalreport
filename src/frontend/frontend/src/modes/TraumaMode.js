import React, { useEffect, useState, useCallback } from 'react';
import Moment from 'react-moment';
import moment from 'moment';
import axios from 'axios';
import { Input, Select, Table, Modal, Button } from 'antd';
import { useTime } from 'react-timer-hook';

// const Image = ({imageName, imageLink, at}) => {
//
//     return <div>
//         <a target="_blank" rel="noopener noreferrer" href={imageLink}>
//             {imageName} - <Moment date={at} format={'DD-MM-YYYY'}/>
//         </a>
//     </div>
// }
// const Images = ({patient}) => {
//     const [images, setImages] = useState([]);
//     useEffect(() => {
//         axios.get(`/api/trauma/images/${patient}`).then(response => {
//             setImages(response.data)
//         })
//     }, [patient])
//
//     return images.map(image => <Image {...image}/>)
// }
const Surgery = ({ surgeryName, at }) => {
  return (
    <div style={{ whiteSpace: 'pre-line' }}>
      {surgeryName} : <Moment date={at} format={'DD-MM-YYYY'} />
    </div>
  );
};
const Surgeries = ({ patient }) => {
  const [surgeries, setSurgeries] = useState([]);
  useEffect(() => {
    axios.get(`/api/trauma/surgeries/${patient}`).then((response) => {
      setSurgeries(response.data);
    });
  }, [patient]);

  return surgeries.map((surgery) => <Surgery {...surgery} />);
};
const AllSurgeries = ({ patientId }) => {
  const [isModalOpenSurgeries, setIsModalOpenSurgeries] = useState(false);
  const [surgeries, setSurgeries] = useState([]);
  const [patientID, setPatientID] = useState(null);
  const showModal = (id) => {
    setPatientID(id);
    setIsModalOpenSurgeries(true);
  };

  const handleOk = () => {
    setPatientID(null);
    setIsModalOpenSurgeries(false);
  };

  const handleCancel = () => {
    setPatientID(null);
    setIsModalOpenSurgeries(false);
  };

  useEffect(() => {
    axios.get(`/api/trauma/surgeries/${patientId}`).then((response) => {
      setSurgeries(response.data);
    });
  }, [patientId]);
  return surgeries.length ? (
    <>
      <Modal
        title="כל הניתוחים"
        open={isModalOpenSurgeries}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="סגור"
        cancelButtonProps={{ style: { display: 'none' } }}
        width="1"
      >
        <Surgeries patient={patientID} />
      </Modal>
      <div>
        <Button type={'text'} onClick={() => showModal(patientId)}>
          הצג את כלל הניתוחים של המטופל
        </Button>
      </div>
    </>
  ) : (
    <div>אין ניתוחים למטופל</div>
  );
};
// const AllImages = ({patientId}) => {
//     const [isModalOpenAllImages, setIsModalOpenAllImages] = useState(false);
//     const [images, setImages] = useState([]);
//     const [patientID, setPatientID] = useState(null);
//     const showModal = (id) => {
//         setPatientID(id)
//         setIsModalOpenAllImages(true);
//
//     };
//
//     const handleOk = () => {
//         setPatientID(null)
//         setIsModalOpenAllImages(false);
//
//     };
//
//     const handleCancel = () => {
//         setPatientID(null)
//         setIsModalOpenAllImages(false);
//
//     };
//
//     useEffect(() => {
//         axios.get(`/api/trauma/images/${patientId}`).then(response => {
//             setImages(response.data)
//         })
//     }, [patientId])
//     return images.length ?
//         <>
//
//             <Modal title="כל ההדמיות" open={isModalOpenAllImages} onOk={handleOk}
//                    onCancel={handleCancel} okText="סגור"
//                    cancelButtonProps={{style: {display: 'none'}}} width="1">
//                 <Images patient={patientID}/>
//
//             </Modal>
//             <div>
//                 <a onClick={() => showModal(patientId)}>הצג את כלל ההדמיות של המטופל</a>
//             </div>
//         </>
//         :
//         <div>אין הדמיות למטופל</div>
//
//
// }

const unique = (list) => {
  let res = [];
  list.forEach((item) => {
    if (!res.includes(item)) res.push(item);
  });
  return res;
};
export const Results = () => {
  const [{ loadingData, dataSource }, setData] = useState({ loadingData: false, dataSource: [] });

  const updateData = useCallback(() => {
    setData((prevState) => ({ loadingData: true, dataSource: prevState.dataSource }));
    axios
      .get(`/api/trauma/records`, {})
      .then((response) => {
        setData({ loadingData: false, dataSource: response.data });
      })
      .catch((error) => {
        setData({ loadingData: false, dataSource: [] });
      });
  }, []);

  const { minutes } = useTime();
  useEffect(() => {
    updateData();
  }, [minutes, updateData]);

  const [filterID, setFilterID] = useState(null);
  const [filterName, setFilterName] = useState(null);
  const [filterDepartmentName, setFilterDepartmentName] = useState(null);

  const filteredData = dataSource
    .filter((item) => [undefined, null, ''].includes(filterID) || item.id.toString().includes(filterID))
    .filter((item) => [undefined, null, ''].includes(filterName) || item.name.toString().includes(filterName))
    .filter(
      (item) => [undefined, null, ''].includes(filterDepartmentName) || item.DepartmentName === filterDepartmentName,
    )
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <Table
      size={'small'}
      pagination={filteredData.length > 100 ? { pageSize: 100 } : false}
      style={{ flex: 1, height: '100%', zIndex: 2, border: 'black' }}
      loading={loadingData}
      dataSource={filteredData}
      scroll={{ y: '100%' }}
      bordered
      columns={[
        {
          title: () => (
            <span>
              ת.ז.&nbsp;&nbsp;
              <Input allowClear onChange={(e) => setFilterID(e.target.value)} />
            </span>
          ),
          key: 'id',
          width: '12%',
          render: (row) => (
            <div>
              <a
                target="_blank"
                rel="noopener noreferrer"
                href={`https://timeline.arc-prod.sheba.gov.il/timeline/${row.id}`}
              >
                {row.id}
              </a>
            </div>
          ),
        },
        {
          title: () => (
            <span>
              שם&nbsp;&nbsp;
              <Input allowClear onChange={(e) => setFilterName(e.target.value)} />
            </span>
          ),
          dataIndex: 'name',
        },
        {
          title: 'תאריך קבלה לביה"ח',
          key: 'HospitalAdmission',
          sorter: (a, b) => (moment(a.HospitalAdmission).isBefore(b.HospitalAdmission) ? 1 : -1),
          render: (row) => <Moment date={row.HospitalAdmission} format={'DD-MM-YYYY'} />,
        },
        {
          title: () => (
            <span>
              מחלקה נוכחית&nbsp;&nbsp;&nbsp;
              <Select
                allowClear
                showSearch
                placeholder={'בחר.י מחלקה נוכחית'}
                loading={loadingData}
                value={filterDepartmentName}
                onChange={setFilterDepartmentName}
                style={{ width: '150px' }}
                options={unique(dataSource.map(({ DepartmentName: department }) => department)).map((baseUnit) => ({
                  label: baseUnit,
                  value: baseUnit,
                }))}
                filterOptions={(input, option) => option.label.includes(input)}
              />
            </span>
          ),
          dataIndex: 'DepartmentName',
        },
        {
          title: 'מחלקות שעבר',
          key: 'DepartmentNames',
          render: (row) => (
            <div style={{ whiteSpace: 'pre-line' }}>{row.DepartmentNames.split(',').slice(1).join('\n')}</div>
          ),
        },
        {
          title: 'ניתוחים שבוצעו',
          // width: '4%',
          key: 'surgeries',
          render: (row) => <AllSurgeries patientId={row.id} />,
        },
        // {
        //     title: "הדמיות שבוצעו",
        //     key: "images",
        //     visible: false,
        //     render: row =>  <AllImages patientId={row.id}/>
        //
        // },
        {
          title: 'אבחנה בקבלה',
          key: 'diagnosis',
          ellipsis: true,
          render: (row) => (row.diagnosis ? row.diagnosis : <div>אין אבחנות בקבלה</div>),
        },
      ]}
    />
  );
};

export const TraumaMode = ({}) => {
  return <Results />;
};
