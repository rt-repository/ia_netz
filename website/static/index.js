
function deleteMember(memberId) {
  fetch("/delete-member", {
    method: "POST",
    body: JSON.stringify({ memberId: memberId }),
  }).then((_res) => {
    window.location.href = "/memberlist";
  });
}

function deleteAvailability(availabilityId) {
  fetch("/delete-availability", {
    method: "POST",
    body: JSON.stringify({ availabilityId: availabilityId }),
  }).then((_res) => {
    window.location.href = "/availability";
  });
}

  
  