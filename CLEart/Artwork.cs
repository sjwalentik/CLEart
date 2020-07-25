using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace CLEart
{
    public class Art
    {
        public Artworks artworks;

        public Art()
        {
            readJSONfile();
        }

        public void readJSONfile()
        {
            var myJsonString = File.ReadAllText("data.txt");

            artworks = JsonConvert.DeserializeObject<Artworks>(myJsonString);
        }
    }
          

    public class Artworks
    {
        public List<Artwork> listOfArt { get; set; }
    }

    public class Artwork
    {
        public string id { get; set; }
        public string Accession_number { get; set; }
        public string Title { get; set; }
        public string Tombstone { get; set; }
        public Department[] departments { get; set; }
        public Creator[] creators { get; set; }
    }

    public class Department
    {
        public string id { get; set; }
        public string name { get; set; }
    }

    public class Creator
    {
        public string id { get; set; }
        public string role { get; set; }
        public string description { get; set; }
    }





}
