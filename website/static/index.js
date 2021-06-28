
function deleteMember(memberId) {
  fetch("/delete-member", {
    method: "POST",
    body: JSON.stringify({ memberId: memberId }),
  }).then((_res) => {
    window.location.href = "/memberlist";
  });
}

  
  