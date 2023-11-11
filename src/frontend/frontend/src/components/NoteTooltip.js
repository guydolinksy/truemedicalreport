import { RelativeTime } from './RelativeTime';
import React from 'react';
import { Tooltip } from 'antd';

export const NoteTooltip = ({ placeholder, note, notes, children }) => {
  return (
    <Tooltip
      overlayStyle={{ maxWidth: '50vw' }}
      overlay={
        note || notes ? (
          <div style={{ maxHeight: '50vh', overflowY: 'auto' }}>
            {(notes || []).concat(note || []).map((note, i) =>
              (i !== 0 ? [<br key={`br-${i}`} />] : []).concat([
                <div key={`title-${i}`}>
                  {note.by} {note.subject ? `- ${note.subject} ` : ''}(<RelativeTime date={note.at} />
                  ):
                </div>,
                <div key={`content-${i}`}>{note.content}</div>,
              ]),
            )}
          </div>
        ) : (
          placeholder
        )
      }
    >
      {children}
    </Tooltip>
  );
};
